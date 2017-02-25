
import glob
import os
import pickle

import numpy


from nlp.clustering import features, nmf


MATRIX_FILES = [

    'allwords', 'docwords', 'doctitles',

    'wordmatrix', 'wordvec',

    'vectors',

    # 'weights', 'feat',
]
WH_FILES = [
    'weights', 'feat',
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

    def __init__(self, path: str = None, featcount: int = None):
        """
        """
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise ValueError(path)

        self.featcount = featcount

        matrix_path = os.path.normpath(os.path.join(path, 'matrix'))
        corpus_path = os.path.normpath(os.path.join(path, 'corpus'))

        if not os.path.isdir(corpus_path):
            raise RuntimeError(corpus_path)

        self.path = dict(path=path, matrix=matrix_path, corpus=corpus_path)

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

    def call_factorize(self, iterate=50, feature_number=20):
        """ Removes the weights and features and call matrix.
        """
        self.delete_matrices('weights', 'feat')
        self.__factorize(iterate=iterate, feature_number=feature_number)

    def get_feature_number(self):
        """ Returns the number of features that has been retrieved from the
            corpus.
        """
        return len(self.feat)

    def file_path(self, filename, featcount: int = None):

        if filename not in MATRIX_FILES + WH_FILES:
            raise ValueError(filename)
        if filename in WH_FILES:
            if not featcount:
                raise RuntimeError(filename)
            return os.path.normpath(
                os.path.join(
                    self.path['matrix'], 'wf', str(featcount), filename
                )
            )
        return os.path.normpath(
            os.path.join(self.path['matrix'], '{}'.format(filename))
        )

    def mkdir_mtrx(self):
        """ Making the directory for matrix files. """
        os.makedirs(os.path.join(self.path['matrix']))

    def file_integrity_check(self):
        """ Checking whether all files exist. """

        files = [self._matrix_name(_) for _ in self._matrix_files()]
        return all(_ in files for _ in MATRIX_FILES)

    def make_matrices(self):
        """ Making and saving to disk all matrices. """
        self.__get_words()
        self.__makematrix()
        self.__make_vectors()
        self.__factorize()

    def make_file(self, data: list, objname: str, featcount: int = None):
        """ Creating a file that will hold an array, numpy array type or
            a dict.
        """
        if objname in WH_FILES:
            path = self.file_path(objname, featcount=featcount)
            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
        else:
            path = self.file_path(objname)

        if isinstance(data, (numpy.ndarray, numpy.generic,)):
            ext = 'npy'
            numpy.save('{}.{}'.format(path, ext), data, fix_imports=False)
        else:
            ext = 'pickle'
            pickle.dump(data, open('{}.{}'.format(path, ext), 'wb+'))

    def load_wh_array(self, arrayname, featcount: int = 10):

        extension = 'npy'
        path = '{}.{}'

        return numpy.load(path)

    def load_array(self, arrayname, with_numpy=True, featcount: int = None):
        """ Loading an array from file. """
        extension = 'npy' if with_numpy else 'pickle'
        if arrayname in WH_FILES:
            _ = self.file_path(arrayname, featcount=featcount)
        else:
            _ = self.file_path(arrayname)
        path = '{}.{}'.format(_, extension)

        if with_numpy:
            return numpy.load(path)
        else:
            return pickle.load(open(path, 'rb'))

    def __get_words(self):
        for _ in zip(features.get_words(),
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

        pass

    def __factorize(self, iterate=50, feature_number=25):
        vectors = self.vectors
        weight, feat = nmf.factorize(vectors, pc=feature_number, iter=iterate)
        for _ in zip((weight, feat), ['weights', 'feat']):
            self.make_file(*_, featcount=self.featcount)

    def _matrix_files(self):
        return glob.glob(os.path.normpath(
            os.path.join(self.path.get('matrix'), '*')))

    def _matrix_name(self, path):
        """ Given a path, returns the name of the matrix. """
        return path.split('/')[-1].split('.')[0]

    def purge_matrixdir(self):
        files = self._matrix_files()
        print(files)

        for item in files:
            print(item)

    def delete_matrices(self, *args):
        """
        """
        files = self._matrix_files()
        for item in files:
            matrix_name = self._matrix_name(item)
            if matrix_name in args:
                os.remove(item)
