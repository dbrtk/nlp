

import numpy
from scipy import sparse


def column_norm(X, by_norm='2'):
    """ Compute the norms of each column of a given matrix

    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix

    Optional Parameters
    -------------------
    by_norm : '2' for l2-norm, '1' for l1-norm.
              Default is '2'.

    Returns
    -------
    numpy.array
    """
    if sparse.issparse(X):
        if by_norm == '2':
            norm_vec = numpy.sqrt(X.multiply(X).sum(axis=0))
        elif by_norm == '1':
            norm_vec = X.sum(axis=0)
        else:
            norm_vec = X.sum(axis=0)
        return numpy.asarray(norm_vec)[0]
    else:
        if by_norm == '2':
            norm_vec = numpy.sqrt(numpy.sum(X * X, axis=0))
        elif by_norm == '1':
            norm_vec = numpy.sum(X, axis=0)
        else:
            norm_vec = numpy.sum(X, axis=0)
        return norm_vec


def normalize_column_pair(W, H, by_norm='2'):
    """ Column normalization for a matrix pair 

    Scale the columns of W and H so that the columns of W have unit norms and 
    the product W.dot(H.T) remains the same.  The normalizing coefficients are 
    also returned.

    Side Effect
    -----------
    W and H given as input are changed and returned.

    Parameters
    ----------
    W : numpy.array, shape (m,k)
    H : numpy.array, shape (n,k)

    Optional Parameters
    -------------------
    by_norm : '1' for normalizing by l1-norm, '2' for normalizing by l2-norm.
              Default is '2'.

    Returns
    -------
    ( W, H, weights )
    W, H : normalized matrix pair
    weights : numpy.array, shape k 
    """
    norms = column_norm(W, by_norm=by_norm)

    toNormalize = norms > 0
    W[:, toNormalize] = W[:, toNormalize] / norms[toNormalize]
    H[:, toNormalize] = H[:, toNormalize] * norms[toNormalize]

    weights = numpy.ones(norms.shape)
    weights[toNormalize] = norms[toNormalize]
    return (W, H, weights)
