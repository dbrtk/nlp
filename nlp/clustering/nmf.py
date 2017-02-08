
import random

import numpy


def difcost(a, b):
    dif = 0
    # Loop over every row and column in the matrix
    for i in range(numpy.shape(a)[0]):
        for j in range(numpy.shape(a)[1]):
            # Add together the differences
            dif += pow(a[i, j] - b[i, j], 2)
    return dif


def factorize(v, pc=10, iter=50):
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
