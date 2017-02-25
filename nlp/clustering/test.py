

import pprint

import numpy

from nlp.clustering import clusters, features, nmf, views
from nlp.clustering.data import CorpusMatrix


PRINTER = pprint.PrettyPrinter(indent=4)


def get_features_old():

    _ = '/home/dominik/Desktop/wiki/test/corpus'
    features.set_corpus(_)

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    v = numpy.matrix(wordmatrix)
    weights, feat = nmf.factorize(v, pc=25, iter=50)

    topp, pn = features.showfeatures(weights, feat, articletitles, wordvec)
    features.showarticles(articletitles, topp, pn)


def get_features_with_data(featcount: int = 5):

    # _ = '/home/dominik/Desktop/wiki/test'
    _ = '/home/dominik/www/nlpdata/corpora/58b089d8e032396b01092385/'
    data = CorpusMatrix(path=_, featcount=featcount)

    # features.set_corpus(_)

    # allwords, articlewords, articletitles = features.get_words()

    # wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    # v = numpy.matrix(wordmatrix)
    # v = data.vectors
    # print(v)
    # weights, feat = nmf.factorize(v, pc=25, iter=50)

    # json_obj, topp, pn = views.features_to_json(
    #     data.weights, data.feat, data.doctitles, data.wordvec)

    # # features.showarticles(articletitles, topp, pn)

    # PRINTER.pprint(json_obj)
    data()
    data.call_factorize(feature_number=featcount, iterate=200)
    print('should have 20 features')
    json_obj, topp, pn = views.features_to_json(
        data.weights, data.feat, data.doctitles, data.wordvec)
    PRINTER.pprint(json_obj)
    print(len(json_obj))


def get_features():

    _ = '/home/dominik/Desktop/wiki/tinytiny/corpus/'
    # _ = '/home/dominik/www/nlpdata/corpora/58a315fae032394f90e4b8f8/'
    features.set_corpus(_)

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    v = numpy.matrix(wordmatrix)
    weights, feat = nmf.factorize(v, pc=20, iter=50)

    json_obj, topp, pn = views.features_to_json(
        weights, feat, articletitles, wordvec,
        feature_words=10, docs_per_feature=10)

    # topp, pn = features.showfeatures(
    #     weights, feat, articletitles, wordvec, feature_words=10)

    # features.showarticles(articletitles, topp, pn)

    PRINTER.pprint(json_obj)

    # docs = views.docs_to_json(articletitles, topp, pn, features_per_doc=5)
    # PRINTER.pprint(docs)


def kmeans_clust():
    # _ = '/home/dominik/www/nlpdata/corpora/58a315fae032394f90e4b8f8/'
    _ = '/home/dominik/Desktop/wiki/tinytiny/'
    kclust = views.kmeans_clust(_)
    print(kclust)
    for i in kclust:
        print(i)
        print('\n')


def purge():
    data = CorpusMatrix(path='/home/dominik/Desktop/wiki/tinytiny/')
    # data.purge_matrixdir()
    data.delete_matrices('weights', 'feat')


if __name__ == "__main__":

    get_features_with_data()
    # purge()
