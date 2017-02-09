

import numpy

from nlp.clustering import clusters, features, nmf, views


def get_features():

    _ = '/home/dominik/Desktop/wiki/tiny/'
    features.set_corpus(_)

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    v = numpy.matrix(wordmatrix)
    weights, feat = nmf.factorize(v, pc=25, iter=50)

    topp, pn = features.showfeatures(weights, feat, articletitles, wordvec)
    features.showarticles(articletitles, topp, pn)


def kmeans_clust():

    _ = '/home/dominik/Desktop/wiki/tiny/'
    kclust = views.kmeans_clust(_)
    print(kclust)
    for i in kclust:
        print(i)
        print('\n')


if __name__ == "__main__":

    # kmeans_clust()
    get_features()
