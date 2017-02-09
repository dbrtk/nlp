

from . import clusters, features


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
