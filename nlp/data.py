
import glob
import json
import os
import pathlib
import pickle
import shutil
import stat

import numpy

from . import features
from .config.appconf import DATA_FOLDER, MATRIX_FOLDER, TEXT_FOLDER
from .errors import MatrixFileDoesNotExist
from .emit import extract_features
from .word_count import get_words

MATRIX_FILES = [

    'allwords', 'docwords', 'doctitles', 'lemma',

    'wordmatrix', 'wordvec',

    'vectors',
]

FILE_EXTENSIONS = {

    'allwords': 'pickle',
    'docwords': 'pickle',
    'doctitles': 'pickle',
    'lemma': 'json',

    'wordmatrix': 'pickle',
    'wordvec': 'pickle',

    'vectors': 'npy',

    'weights': 'npy',
    'feat': 'npy'
}

WH_FILES = [
    'weights', 'feat',
]
KMEANS_FILES = [

    'bestmatches'
]


class DataFolder(object):

    @property
    def allwords(self):

        return self.load_array('allwords', with_numpy=False)

    @property
    def docwords(self):

        return self.load_array('docwords', with_numpy=False)

    @property
    def doctitles(self):

        return self.load_array('doctitles', with_numpy=False)

    @property
    def wordmatrix(self):

        return self.load_array('wordmatrix', with_numpy=False)

    @property
    def wordvec(self):

        return self.load_array('wordvec', with_numpy=False)

    @property
    def vectors(self):

        return self.load_array('vectors')

    @property
    def lemma_to_dict(self):

        path = '{}.json'.format(self.file_path('lemma'))
        out = {}
        with open(path, 'r') as _file:
            for _line in _file.readlines():
                _obj = json.loads(_line)
                out[_obj.get('lemma')] = _obj.get('words')
        return out

    @property
    def weights(self):

        return self.load_array('weights', featcount=self.featcount)

    @property
    def feat(self):

        return self.load_array('feat', featcount=self.featcount)

    @property
    def available_feats(self):
        path = os.path.join(self.path.get('matrix'), 'wf')

        if not os.path.isdir(path):
            return []

        old_fcount = self.featcount
        dirs = os.listdir(path)

        out = []
        for _ in dirs:
            self.featcount = int(_)
            _path = os.path.join(path, _)
            wf_content = os.listdir(_path)
            if not all(_ in wf_content for _ in ['feat.npy', 'weights.npy']):
                continue
            out.append(dict(
                featcount=_,
                path=_path,
                feat=os.path.join(_path, 'feat.npy'),
                weights=os.path.join(_path, 'weights.npy')
            ))
        self.featcount = old_fcount
        return out

    def __init__(self,
                 path: str = None,
                 featcount: int = 10,
                 containerid: str = None):
        """
        """
        if not path:
            path = os.path.join(DATA_FOLDER, containerid)
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            self.make_corpus_dir(path)
        self.containerid = containerid
        self.featcount = featcount

        matrix_path = os.path.normpath(os.path.join(path, MATRIX_FOLDER))
        text_path = os.path.normpath(os.path.join(path, TEXT_FOLDER))

        self.path = dict(path=path, matrix=matrix_path, text=text_path)

        if not os.path.isdir(text_path):
            self.mkdir_corpus()

        # setting up the path to the corpus on the level of features module.
        features.set_corpus(self.path['text'])

        if not os.path.isdir(matrix_path):
            self.mkdir_mtrx()

    def __call__(self):
        """
        """
        if not isinstance(self.featcount, int):
            raise RuntimeError(self)
        if not self.file_integrity_check():
            self.make_matrices()

    def call_factorize(self, purge=False):
        """ Removes the weights and features and calls the matrix generator.
        """
        if purge:
            self.delete_matrices('weights', 'feat')
        self.__factorize()

    def feat_weights_path(self, create: bool = False):
        """
        Returns the path of the folder that holds matrices containing features
        weights.
        :param create:
        :return:
        """
        path = os.path.normpath(
            os.path.join(
                self.path['matrix'], 'wf', str(self.featcount)
            )
        )
        if create:
            if not os.path.exists(path):
                os.makedirs(path)
        return path

    def file_path(self, filename, featcount: int = None):

        if filename not in MATRIX_FILES + WH_FILES:  # + KMEANS_FILES:
            raise MatrixFileDoesNotExist(filename)
        if filename in WH_FILES:
            if not featcount:
                raise RuntimeError(filename)
            return os.path.normpath(
                os.path.join(
                    self.path['matrix'], 'wf', str(featcount), filename
                )
            )
        if filename in KMEANS_FILES:
            return os.path.normpath(
                os.path.join(
                    self.path['matrix'], 'kmeans', str(featcount), filename
                )
            )
        return os.path.normpath(
            os.path.join(self.path['matrix'], '{}'.format(filename))
        )

    def chmod_fd(self, path):
        """ Setting up permissions on the files and directories. Because of
            celery and apache, these owe to be 777 for all.
        """
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def make_corpus_dir(self, path):
        """Making a directory that will hold the files, including the corpus
           and the matrix files.
        """
        os.makedirs(path)
        self.chmod_fd(path)

    def mkdir_mtrx(self):
        """ Making the directory for matrix files. """
        _wf = os.path.join(self.path['matrix'], 'wf')
        os.makedirs(_wf)
        self.chmod_fd(self.path['matrix'])
        self.chmod_fd(_wf)

    def mkdir_corpus(self):
        """ Making the directory for corpus files. """
        path = self.path['text']
        os.makedirs(path)
        self.chmod_fd(path)

    def file_integrity_check(self):
        """ Checking whether all files exist. """

        files = [self._matrix_name(_) for _ in self._matrix_files()]
        return all(_ in files for _ in MATRIX_FILES)

    def make_matrices(self):
        """ Making and saving to disk all the matrices necessary to . """

        self.__get_words()
        self.compute_matrices()

    def compute_matrices(self):
        """Computing matrices after the corpus has been changed."""
        self.__makematrix()
        self.__make_vectors()

    def remove_file(self, objname):
        """Removing the file that matches an object name."""
        path = '{}.{}'.format(self.file_path(objname),
                              FILE_EXTENSIONS[objname])
        return os.remove(path)

    def make_file(self, data: (numpy.ndarray, list), objname: str,
                  featcount: int = None, ext: str = None):
        """ Creating a file that will hold an array, numpy array type or
            a dict.
        """
        if objname in WH_FILES:
            path = self.file_path(objname, featcount=featcount)
            parentpath = os.path.dirname(path)

            if not os.path.isdir(parentpath):
                os.makedirs(parentpath)
                self.chmod_fd(parentpath)
        else:
            path = self.file_path(objname)
        if not ext:
            if isinstance(data, (numpy.ndarray, numpy.generic,)):
                ext = 'npy'
                numpy.save('{}.{}'.format(path, ext), data, fix_imports=False)
            else:
                ext = 'pickle'
                pickle.dump(data, open('{}.{}'.format(path, ext), 'wb+'))
        if ext == 'json':
            self.write_json_list(data, '{}'.format(path))
        self.chmod_fd('{}.{}'.format(path, ext))

    def write_json_list(self, data, path):
        """ Writing a list of dictionaries to a csv file. """
        with open('{}.{}'.format(path, 'json'), 'w+') as _file:
            _file.writelines('{}\n'.format(json.dumps(_)) for _ in data)

    def load_array(self, arrayname, with_numpy=True, featcount: int = None):
        """ Loading an array from file. """
        extension = 'npy' if with_numpy else 'pickle'
        if arrayname in WH_FILES:
            _ = self.file_path(arrayname, featcount=featcount)
        else:
            _ = self.file_path(arrayname)
        path = '{}.{}'.format(_, extension)

        if not os.path.exists(path):
            raise MatrixFileDoesNotExist(path)
        if with_numpy:
            return numpy.load(pathlib.Path(path))
        return pickle.load(open(path, 'rb'))

    def __get_words(self):
        for _ in zip(get_words(self.path['text']),
                     ['allwords', 'docwords', 'doctitles', 'lemma']):

            kwds = {}
            if _[1] == 'lemma':
                kwds['ext'] = 'json'
            self.make_file(*_, **kwds)

    def __makematrix(self):

        allwords = self.allwords
        docwords = self.docwords

        wordmatrix, wordvec = features.makematrix(allwords, docwords)

        self.make_file(wordmatrix, 'wordmatrix')
        self.make_file(wordvec, 'wordvec')

    def __make_vectors(self):

        wordmatrix = self.wordmatrix
        v = numpy.matrix(wordmatrix)
        self.make_file(v, 'vectors')

    def check_wf_folder_structure(self) -> bool:
        """
        Verifying the structure of the folder that holds features and weights.
        :return: bool
        """
        expected_files = {
            f'{_}.{FILE_EXTENSIONS[_]}' for _ in WH_FILES
        }
        path = self.feat_weights_path()
        files = os.listdir(path)
        if not set(files) == expected_files:
            shutil.rmtree(path)
            return False
        for item in files:
            try:
                numpy.load(os.path.join(path, item))
            except (IOError, ValueError):
                shutil.rmtree(path)
                return False
        return True

    def chmod_wf(self):
        """
        This is a function that will chmod the created "wf" folder.
        :return:
        """
        path = self.feat_weights_path()
        self.chmod_fd(path)
        for _ in os.listdir(path):
            self.chmod_fd(os.path.join(path, _))

    def __factorize(self) -> None:
        """
        Factorize the matrix using rmxnmf - which is an external service.

        :return:
        """
        ftype = 'vectors'

        extract_features(
            containerid=self.containerid,
            feature_number=self.featcount,
            matrix_path=f'{self.file_path(ftype)}.{FILE_EXTENSIONS[ftype]}',
            target_path=self.feat_weights_path(create=True),
            path=self.path.get('path')
        )

    def _matrix_files(self):
        return glob.glob(os.path.normpath(
            os.path.join(self.path.get('matrix'), '*')))

    def _matrix_name(self, path):
        """ Given a path, returns the name of the matrix. """
        return path.split('/')[-1].split('.')[0]

    def delete_matrices(self, *args):
        """
        """
        files = self._matrix_files()
        for item in files:
            matrix_name = self._matrix_name(item)
            if matrix_name in args:
                os.remove(item)

    def purge_matrix(self): return shutil.rmtree(self.path.get('matrix'))

    def kmeans_files(self):
        """returns file paths for the k-means cluster"""

        return {
            'wordmatrix': "{}.{}".format(
                self.file_path(filename='wordmatrix'),
                FILE_EXTENSIONS['wordmatrix']),
            'doctitles': "{}.{}".format(
                self.file_path(filename='doctitles'),
                FILE_EXTENSIONS['doctitles'])
        }
