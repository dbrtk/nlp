
import numpy

from . import clusters, features
from .data import DataFolder


def kmeans_clust(containerid, path, k: int = 10):
    """
    Given a container and the number of groups (k), returns data for a kmeans
    cluster.
    """
    inst = DataFolder(containerid=containerid, path=path, featcount=k)
    return clusters.get_clusters(
        clusters.kcluster(inst.wordmatrix, k=k), inst.doctitles)


def features_to_json(weights, features, titles, wordvec, feature_words: int = 6,
                     docs_per_feature: int = 3):
    """
    :param weights: weights - numpy.ndarray
    :param features: features - numpy.ndarray
    :param titles:
    :param wordvec:
    :param feature_words:
    :param docs_per_feature:
    :return:
    """
    out = []

    # from celery.contrib import rdb
    # rdb.set_trace()

    feature_words = int(feature_words)
    docs_per_feature = int(docs_per_feature)
    pc, wc = numpy.shape(features)
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []
    # Loop over all the features
    for i in range(pc):
        f_obj = {}

        # Create a list of words and their weights
        slist = []
        for j in range(wc):
            slist.append((features[i, j], wordvec[j]))
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
            flist.append((weights[j, i], titles[j]))
            toppatterns[j].append((weights[j, i], i, titles[j]))

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
    # Return the pattern names for later use
    return out, toppatterns, patternnames


def docs_to_json(titles, toppatterns, patternnames, features_per_doc=3):
    output = []
    features_per_doc = int(features_per_doc)
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
                      containerid: str = None,
                      words: int = 6,
                      docs_per_feat: int = 3,
                      feats_per_doc: int = 3) -> (None, tuple):
    """ Returning features and docs. This method will compute all the matrices. """

    data = DataFolder(path=path, featcount=feats, containerid=containerid)
    data()
    available_feats = data.available_feats
    try:
        next(_.get('featcount') for _ in available_feats
             if feats == int(_.get('featcount')))
    except StopIteration:
        data.call_factorize()
        return

    json_obj, topp, pn = features_to_json(
        data.weights, data.feat, data.doctitles, data.wordvec,
        feature_words=words, docs_per_feature=docs_per_feat)

    docs_obj = docs_to_json(data.doctitles, topp, pn,
                            features_per_doc=feats_per_doc)

    return json_obj, docs_obj


def call_factorize(path: str = None,
                   feats: int = 25,
                   corpusid: str = None,
                   words: int = 6,
                   docs_per_feat: int = 3,
                   feats_per_doc: int = 3):
    """ This function is called to factorize matrices, given a features number. """
    data = DataFolder(path=path, featcount=feats, containerid=corpusid)
    data.call_factorize()
    return True
