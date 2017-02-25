

import numpy

from . import clusters, features, nmf
from .data import CorpusMatrix


def simple_dendogram():
    """A simple json for testing purposes."""
    features.set_corpus('/home/dominik/Desktop/wiki/tiny/')

    allwords, articlewords, articletitles = features.get_words()

    wordmatrix, wordvec = features.makematrix(allwords, articlewords)
    clust = clusters.hcluster(wordmatrix)
    clust, depth = clusters.hcluster_to_json(clust, labels=articletitles)

    return clust, depth


def kmeans_clust(corpus_path):
    """For a given corpora, returns a kmeans cluster.
    """
    features.set_corpus(corpus_path)
    allwords, articlewords, articletitles = features.get_words()
    wordmatrix, wordvec = features.makematrix(allwords, articlewords)
    return clusters.get_clusters(
        clusters.kcluster(wordmatrix, k=10), articletitles)


def independent_features(corpus_path: str = None, features_count: int = 10):
    """ Extracting independent features form the corpus. """

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
        # Print the top three patterns
        for i in range(features_per_doc):
            doc['weight'] = toppatterns[j][i][0]
            doc['feature'] = patternnames[toppatterns[j][i][1]]
        output.append(doc)
    return output


def features_and_docs(path: str = None,
                      feature_number: int = 25,
                      feature_words: int = 6,
                      docs_per_feature: int = 3,
                      features_per_doc: int = 3):
    """ Returning features and docs. """
    data = CorpusMatrix(path=path, featcount=feature_number)
    data()

    if data.get_feature_number() != feature_number:
        print(feature_number)
        data.call_factorize(feature_number=feature_number)

    json_obj, topp, pn = features_to_json(
        data.weights, data.feat, data.doctitles, data.wordvec,
        feature_words=feature_words, docs_per_feature=docs_per_feature)

    docs_obj = docs_to_json(data.doctitles, topp, pn,
                            features_per_doc=features_per_doc)

    return json_obj, docs_obj


def get_features_count(path: str = None):
    """ Returns the feature number that have been computed for this corpus. """
    return CorpusMatrix(path=path).available_feats


def get_matrices(path: str = None):
    pass
