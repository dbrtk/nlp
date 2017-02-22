
import random

import numpy
from nlp.clustering.optimization import annealing_features


def _costfun(v, wh):
    dif = 0
    for i in range(len(v)):
        dif += pow(v[i] - wh[i], 2)
    return dif


def make_domain(v, wh):
    cols = numpy.shape(v)[1]
    v = v.tolist()[0]
    wh = wh.tolist()[0]
    return [(0, pow(v[_] + wh[_], 2)) for _ in range(cols)]


def neo_difcost(v, wh):
    dif = 0
    # Loop over every row and column in the matrix
    for i in range(numpy.shape(v)[0]):
        domain = make_domain(v[i], wh[i])
        print('domain:')
        print(domain)
        vec = []
        for j in range(numpy.shape(v)[1]):
            # cost = annealing_features((a[i, j] - b[i, j]), domain, costf)
            # Add together the differences
            vec.append(float(v[i, j].astype(int) - wh[i, j].astype(int)))
            # dif += pow(v[i, j] - wh[i, j], 2)
        print('vec:')
        print(vec)
        print('wh')
        _wh = wh[i].tolist()[0]
        s = annealing_features(vec, _wh, domain, _costfun)
        print(s)
        # s = _costfun(s, wh)
        # print(s)
        # dif += s
    return dif


def difcost(a, b):
    dif = 0
    # Loop over every row and column in the matrix
    for i in range(numpy.shape(a)[0]):
        for j in range(numpy.shape(a)[1]):
            # Add together the differences
            dif += pow(a[i, j] - b[i, j], 2)
    return dif


def factorize(v, pc=10, iter=50):
    """
    """
    ic = numpy.shape(v)[0]
    fc = numpy.shape(v)[1]
    # Initialize the weight and feature matrices with random values
    w = numpy.matrix([[random.random() for j in range(pc)] for i in range(ic)])
    h = numpy.matrix([[random.random() for i in range(fc)] for i in range(pc)])

    # Perform operation a maximum of iter times
    for i in range(iter):
        wh = w * h

        # Calculate the current difference
        cost = difcost(v, wh)
        # cost = annealing_features(v, wh, neo_difcost)

        if i % 10 == 0:
            print(cost)
        # Terminate if the matrix has been fully factorized
        if cost == 0:
            break

        # Update feature matrix
        hn = (numpy.transpose(w) * v)
        hd = (numpy.transpose(w) * w * h)
        h = numpy.matrix(numpy.array(h) * numpy.array(hn) / numpy.array(hd))
        # Update weights matrix
        wn = (v * numpy.transpose(h))
        wd = (w * h * numpy.transpose(h))
        w = numpy.matrix(numpy.array(w) * numpy.array(wn) / numpy.array(wd))

    return w, h


if __name__ == '__main__':

    m1 = numpy.matrix([[1, 2, 3], [4, 5, 6]])
    m2 = numpy.matrix([[1, 2], [3, 4], [5, 6]])

    print(m1)
    print(m2)

    w, h = factorize(m1 * m2, pc=3, iter=100)

    print(w)
    print(h)
