

import pprint
import numpy
import os
import shutil

from nlp import clusters, features, nmf, views
from nlp.data import CorpusMatrix


PRINTER = pprint.PrettyPrinter(indent=4)


def get_features_old():

    _ = '/path/to/corpus'
    features.set_corpus(_)

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    v = numpy.matrix(wordmatrix)
    weights, feat = nmf.factorize(v, pc=25, iter=50)

    topp, pn = features.showfeatures(weights, feat, articletitles, wordvec)

    features.showarticles(articletitles, topp, pn)


def get_features_with_data(featcount: int = 5):

    _ = '/path/to/corpus/'

    shutil.rmtree(os.path.join(_, 'matrix'))

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

    data.call_factorize(feature_number=featcount)
    print('should have 20 features')
    json_obj, topp, pn = views.features_to_json(
        data.weights, data.feat, data.doctitles, data.wordvec)
    PRINTER.pprint(json_obj)


def get_feats_view():
    path = '/path/to/corpus/'
    try:
        shutil.rmtree(os.path.join(path, 'matrix'))
    except FileNotFoundError:
        pass
    _json, _docs = views.features_and_docs(path, feats=10)
    PRINTER.pprint(_json)


def kmeans_clust():
    _ = '/path/to/corpus/'
    kclust = views.kmeans_clust(_)
    print(kclust)
    for i in kclust:
        print(i)
        print('\n')


def purge():
    data = CorpusMatrix(path='/path/to/corpus/')
    # data.purge_matrixdir()
    data.delete_matrices('weights', 'feat')


def count_feats():
    _ = '/path/to/corpus/'
    data = CorpusMatrix(path=_)
    data.available_feats


if __name__ == "__main__":
    get_features_old()
    # get_feats_view()
