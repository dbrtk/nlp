
import numpy
import random

from .nnls import nnlsm_blockpivot
from .utils import normalize_column_pair


class NMF(object):

    def __init__(self, main_matrix: numpy.matrix = None, init=None,
                 feats_number: int = 10, max_iter: int = 50, max_time=None):

        self.main_matrix = main_matrix
        self.feats_number = feats_number
        self.max_iter = max_iter
        self.max_time = max_time
        self.init = init

    def factorize(self):

        ic = numpy.shape(self.main_matrix)[0]
        fc = numpy.shape(self.main_matrix)[1]

        # Initialize the weight and feature matrices with random values
        weights = numpy.matrix(
            [[random.random() for j in range(self.feats_number)]
             for i in range(ic)])
        features = numpy.matrix([[random.random() for i in range(fc)]
                                 for i in range(self.feats_number)])

        for i in range(self.max_iter):

            (weights, features) = self.iter_solver(
                self.main_matrix,
                weights,
                features,
                self.feats_number,
                i
            )
        weights, features, _ = normalize_column_pair(weights, features)
        return (weights, features)


class WetAss_NMF(object):

    def __init__(self):

        pass


class NMF_MU(object):

    def __init__(self, max_iter=500, max_time=numpy.inf, *args, **kwds):

        super().__init__(*args, **kwds)

        self.eps = 1e-16
        self.max_iter = max_iter
        self.max_time = max_time

    def iter_solver(self, A, W, H, k, it):

        AtW = A.T.dot(W)
        HWtW = H.dot(W.T.dot(W)) + self.eps
        H = H * AtW
        H = H / HWtW

        AH = A.dot(H)
        WHtH = W.dot(H.T.dot(H)) + self.eps
        W = W * AH
        W = W / WHtH

        return (W, H)


class NMF_ANLS_BLOCKPIVOT(NMF):

    def __init__(self, max_iter=50, max_time=numpy.inf):

        self.max_iter = max_iter
        self.max_time = max_time

    def iter_solver(self, A, W, H, k, it):

        Sol, info = nnlsm_blockpivot(W, A, init=H.T)
        H = Sol.T
        Sol, info = nnlsm_blockpivot(H, A.T, init=W.T)
        W = Sol.T
        return (W, H)
