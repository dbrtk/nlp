

import numpy

from . import config, clusters, features, nmf
from .data import CorpusMatrix


def simple_dendogram(path: str = None,
                     feats: int = 25,
                     corpusid: str = None):
    """Returns the data for a dendogram. Used for testing purposes."""

    data = CorpusMatrix(path=path, featcount=feats, corpusid=corpusid)
    data()
    available_feats = data.available_feats
    try:
        next(_.get('featcount') for _ in available_feats
             if feats == int(_.get('featcount')))
    except StopIteration:
        data.call_factorize(feature_number=feats, iterate=config.MAX_ITERATE)

    # todo(): clean-up!
    # todo(): implement the dendogram
    # features.set_corpus(corpus_path)

    # allwords, articlewords, articletitles = features.get_words()
    # wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    clust = clusters.hcluster(data.wordmatrix)
    clust, depth = clusters.hcluster_to_json(clust, labels=data.doctitles)

    return clust, depth


def kmeans_clust(path, k: int = 10):
    """ Given a corpus and the number of groups (k), returns a kmeans cluster.
    """

    # data = CorpusMatrix(path=path)
    # data()
    features.set_corpus(path)
    allwords, articlewords, articletitles = features.get_words()
    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    return clusters.get_clusters(
        clusters.kcluster(wordmatrix, k=k), articletitles)


def independent_features(corpus_path: str = None, features_count: int = 10):
    """ Extracting independent features form the corpus. This function should
        remain in order to keep track of how feature extraction works (calls).
    """

    features.set_corpus(corpus_path)

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)

    v = numpy.matrix(wordmatrix)
    weights, feat = nmf.factorize(v, pc=features_count, iter=50)

    topp, pn = features.showfeatures(weights, feat, articletitles, wordvec)
    features.showarticles(articletitles, topp, pn)


def features_to_json(w, h, titles, wordvec, feature_words: int = 6,
                     docs_per_feature: int = 3):
    out = []
    pc, wc = numpy.shape(h)
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []
    # Loop over all the features
    for i in range(pc):
        f_obj = {}
        slist = []
        # Create a list of words and their weights
        for j in range(wc):
            slist.append((h[i, j], wordvec[j]))
        # Reverse sort the word list
        slist.sort()
        slist.reverse()

        # Print the first six elements
        # n = [s[1] for s in slist[0:6]]
        n = [dict(word=s[1], weight=s[0]) for s in slist[0:feature_words]]
        f_obj['features'] = n

        # outfile.write(str(n) + '\n')
        patternnames.append(n)

        # Create a list of articles for this feature
        flist = []

        for j in range(len(titles)):
            # Add the article with its weight
            flist.append((w[j, i], titles[j]))
            toppatterns[j].append((w[j, i], i, titles[j]))

        # Reverse sort the list
        flist.sort()
        flist.reverse()

        # Show the top 3 articles
        f_obj['docs'] = list(dict(weight=_[0], dataid=_[1])
                             for _ in flist[0:docs_per_feature])

        # for f in flist[0:docs_per_feature]:
        #     outfile.write(str(f) + '\n')
        # outfile.write('\n')
        out.append(f_obj)
    # outfile.close()
    # Return the pattern names for later use
    return out, toppatterns, patternnames


def docs_to_json(titles, toppatterns, patternnames, features_per_doc=3):
    output = []
    # Loop over all the articles
    for j in range(len(titles)):
        doc = dict(dataid=titles[j])
        # Get the top features for this article and
        # reverse sort them
        toppatterns[j].sort()
        toppatterns[j].reverse()
        # Add a variable number  of top features for this document.
        doc['features'] = [dict(
            weight=toppatterns[j][i][0],
            feature=patternnames[toppatterns[j][i][1]]
        ) for i in range(features_per_doc)]

        output.append(doc)
    return output


def features_and_docs(path: str = None,
                      feats: int = 25,
                      corpusid: str = None,
                      words: int = 6,
                      docs_per_feat: int = 3,
                      feats_per_doc: int = 3):
    """ Returning features and docs. """

    data = CorpusMatrix(path=path, featcount=feats, corpusid=corpusid)
    data()
    available_feats = data.available_feats
    try:
        next(_.get('featcount') for _ in available_feats
             if feats == int(_.get('featcount')))
    except StopIteration:
        data.call_factorize(feature_number=feats, iterate=config.MAX_ITERATE)

    json_obj, topp, pn = features_to_json(
        data.weights, data.feat, data.doctitles, data.wordvec,
        feature_words=words, docs_per_feature=docs_per_feat)

    docs_obj = docs_to_json(data.doctitles, topp, pn,
                            features_per_doc=feats_per_doc)

    return json_obj, docs_obj


def get_features_count(path: str = None):
    """ Returns the feature number that have been computed for this corpus. """
    return CorpusMatrix(path=path).available_feats


def remove_feature(**kwds):

    data = CorpusMatrix(**kwds)
    data.remove_featdir()


def generate_matrices(path):
    """ Generating basic matrices. """
    data = CorpusMatrix(path=path)
    vec = data.getnerate_basic_matrices()
    # todo(): check vectors
    return vec
