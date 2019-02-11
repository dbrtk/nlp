
import numpy
from sklearn.decomposition import NMF as NMF_sklearn

from nlp.nnls import nnlsm_blockpivot
from nlp.utils import normalize_column_pair


class NMF(object):

    def __init__(self, main_matrix: numpy.matrix = None, init=None,
                 feats_number: int = 10, max_iter: int = 50, max_time=None):

        self.main_matrix = main_matrix
        self.feats_number = feats_number
        self.max_iter = max_iter
        self.max_time = max_time
        self.init = init

    def iter_solver(self, A, W, H, k, it): raise NotImplemented()

    def factorize(self):

        if self.init is not None:
            weights = self.init[0].copy()
            features = self.init[1].copy()
        else:
            weights = numpy.random.rand(
                self.main_matrix.shape[0], self.feats_number)
            features = numpy.random.rand(
                self.main_matrix.shape[1], self.feats_number)

        for _it in range(self.max_iter):

            (weights, features) = self.iter_solver(
                self.main_matrix,
                weights,
                features,
                self.feats_number,
                _it
            )
        weights, features, _ = normalize_column_pair(weights, features)

        # todo(): transpose the features matrix.
        _features = features.T

        return (weights, _features)


class NMF_with_sklearn(object):

    def __init__(self, main_matrix: numpy.matrix = None, init=None,
                 feats_number: int = 10, max_iter: int = 50, max_time=None):

        self.main_matrix = main_matrix
        self.feats_number = feats_number
        self.max_iter = max_iter
        self.max_time = max_time
        self.init = init

    def factorize(self):

        model = NMF_sklearn(n_components=self.feats_number,
                            init='random', random_state=0)
        W = model.fit_transform(self.main_matrix)
        H = model.components_
        return (W, H)


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

    def __init__(self, *args, **kwds):

        self.max_time = numpy.inf
        super().__init__(*args, **kwds)

    def iter_solver(self, A, W, H, k, it):

        Sol, info = nnlsm_blockpivot(W, A, init=H.T)
        H = Sol.T
        Sol, info = nnlsm_blockpivot(H, A.T, init=W.T)
        W = Sol.T
        return (W, H)


def _test_nmf_anls_blockpivot():

    k = 10
    m, n = 300, 300
    W_org = numpy.random.rand(m, k)
    H_org = numpy.random.rand(n, k)
    A = W_org.dot(H_org.T)
    alg = NMF_ANLS_BLOCKPIVOT(main_matrix=A, feats_number=k, max_iter=100)
    results = alg.factorize()

    return results


if __name__ == '__main__':

    _test_nmf_anls_blockpivot()
