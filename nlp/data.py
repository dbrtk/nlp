
import glob
import os
import pathlib
import pickle
import shutil
import stat

import numpy

from . import features, nmf, simple_nmf
from .word_count import get_words

MATRIX_FILES = [

    'allwords', 'docwords', 'doctitles',

    'wordmatrix', 'wordvec',

    'vectors',

    # 'weights', 'feat',
]
WH_FILES = [
    'weights', 'feat',
]
KMEANS_FILES = [

    'bestmatches'
]
TEMP_MATRICES = [

    'toppatterns', 'patternnames'

]


class CorpusMatrix(object):

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
    def old_weights(self):

        return self.load_array('weights')

    @property
    def old_feat(self):

        return self.load_array('feat')

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
            self.featcount = _

            if not int(_) == len(self.feat):
                continue  # raise RuntimeError(self)

            _path = os.path.join(path, _)
            out.append(dict(
                featcount=_,
                path=_path,
                feat=os.path.join(_path, 'feat.npy'),
                weights=os.path.join(_path, 'weights.npy')
            ))
        self.featcount = old_fcount
        return out

    @property
    def available_kmeans(self):
        path = os.path.join(self.path.get('matrix'), 'kmeans')
        if not os.path.isdir(path):
            return []
        dirs = os.listdir(path)
        out = []
        for _ in dirs:
            _path = os.path.join(path, _)
            out.append(dict(
                k=_,
                path=_path
            ))
        return out

    def __init__(self, path: str = None, featcount: int = None,
                 corpusid: str = None):
        """
        """
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise ValueError(path)
        self.corpusid = corpusid
        self.featcount = featcount

        matrix_path = os.path.normpath(os.path.join(path, 'matrix'))
        corpus_path = os.path.normpath(os.path.join(path, 'corpus'))

        self.path = dict(path=path, matrix=matrix_path, corpus=corpus_path)

        if not os.path.isdir(corpus_path):
            self.mkdir_corpus()
            # raise RuntimeError(corpus_path)

        # setting up the path to the corpus on the level of features module.
        features.set_corpus(self.path['corpus'])

        if not os.path.isdir(matrix_path):
            self.mkdir_mtrx()

    def __call__(self):
        """
        """
        if not isinstance(self.featcount, int):
            raise RuntimeError(self)
        if not self.file_integrity_check():
            self.make_matrices()

    def call_factorize(self, iterate=50, feature_number=20, purge=False):
        """ Removes the weights and features and calls the matrix generator.
        """
        if purge:
            self.delete_matrices('weights', 'feat')
        self.__factorize(iterate=iterate, feature_number=feature_number)

    def get_feature_number(self):
        """ Returns the number of features that has been retrieved from the
            corpus.
        """
        return len(self.feat)

    def file_path(self, filename, featcount: int = None):

        if filename not in MATRIX_FILES + WH_FILES:  # + KMEANS_FILES:
            raise ValueError(filename)
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

    def mkdir_mtrx(self):
        """ Making the directory for matrix files. """
        _wf = os.path.join(self.path['matrix'], 'wf')
        os.makedirs(_wf)
        self.chmod_fd(self.path['matrix'])
        self.chmod_fd(_wf)

    def mkdir_corpus(self):
        """ Making the directory for matrix files. """
        path = self.path['corpus']
        os.makedirs(path)
        self.chmod_fd(path)

    def file_integrity_check(self):
        """ Checking whether all files exist. """

        files = [self._matrix_name(_) for _ in self._matrix_files()]
        return all(_ in files for _ in MATRIX_FILES)

    def make_matrices(self):
        """ Making and saving to disk all the matrices necessary to . """
        self.__get_words()
        self.__makematrix()
        self.__make_vectors()
        self.__factorize()

    def make_file(self, data: (numpy.ndarray, list), objname: str,
                  featcount: int = None):
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

        if isinstance(data, (numpy.ndarray, numpy.generic,)):
            ext = 'npy'
            numpy.save('{}.{}'.format(path, ext), data, fix_imports=False)
        else:
            ext = 'pickle'
            pickle.dump(data, open('{}.{}'.format(path, ext), 'wb+'))
        self.chmod_fd('{}.{}'.format(path, ext))

    def load_array(self, arrayname, with_numpy=True, featcount: int = None):
        """ Loading an array from file. """
        extension = 'npy' if with_numpy else 'pickle'
        if arrayname in WH_FILES:
            _ = self.file_path(arrayname, featcount=featcount)
        else:
            _ = self.file_path(arrayname)
        path = '{}.{}'.format(_, extension)

        if not os.path.exists(path):
            raise ValueError(path)
        if with_numpy:
            return numpy.load(pathlib.Path(path))
        else:
            return pickle.load(open(path, 'rb'))

    def __get_words(self):
        for _ in zip(get_words(self.path['corpus'], corpusid=self.corpusid),
                     ['allwords', 'docwords', 'doctitles']):
            self.make_file(*_)

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

    def feat_weights_nmb(self, featcount: int = 10):
        pass

    def factorize(self, featcount: int = 10):
        """ Calling the factorization with n features. """
        # todo(): delete?
        pass

    def __factorize(self, iterate=50, feature_number=25):
        """Calling the factorization of the matrix in order to retrieve 2
           matrices; 1 containing features; the other one containing weights.
        """
        vectors = self.vectors
        inst = nmf.NMF_ANLS_BLOCKPIVOT(
            max_iter=iterate,
            main_matrix=vectors,
            feats_number=feature_number)

        weight, feat = inst.factorize()

        # weight, feat = simple_nmf.factorize(
        #     vectors, pc=feature_number, iter=iterate)
        for _ in zip((weight, feat), ['weights', 'feat']):
            self.make_file(*_, featcount=self.featcount)

    def __factorize__old(self, iterate=50, feature_number=25):

        # todo(): delete

        vectors = self.vectors
        weight, feat = simple_nmf.factorize(
            vectors, pc=feature_number, iter=iterate)
        for _ in zip((weight, feat), ['weights', 'feat']):
            self.make_file(*_, featcount=self.featcount)

    def _matrix_files(self):
        return glob.glob(os.path.normpath(
            os.path.join(self.path.get('matrix'), '*')))

    def _matrix_name(self, path):
        """ Given a path, returns the name of the matrix. """
        return path.split('/')[-1].split('.')[0]

    def purge_matrixdir(self):
        # shutil.rmtree(self.path['matrix'])
        files = self._matrix_files()
        for item in files:
            pass

    def delete_matrices(self, *args):
        """
        """
        files = self._matrix_files()
        for item in files:
            matrix_name = self._matrix_name(item)
            if matrix_name in args:
                os.remove(item)

    def remove_featdir(self):
        path = os.path.join(self.path.get('matrix'), 'wf', str(self.featcount))
        if os.path.isdir(path):
            shutil.rmtree(path)

    def getnerate_basic_matrices(self):
        vectors = self.vectors
        self.file_integrity_check()
        return vectors
