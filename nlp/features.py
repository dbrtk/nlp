
import os
import re

import numpy

from . import clusters


CORPUSPATH = '/path/to/container'


def separatewords(text):
    # splitter = re.compile('\\W*')
    splitter = re.compile(r'\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


def get_words(container: str = None) -> (dict, list, list):
    """Getting the words from a given text container."""
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0

    for item in os.listdir(container or CORPUSPATH):
        path = os.path.normpath(os.path.join(CORPUSPATH, item))

        _file = open(path, 'r')

        txt = _file.read()
        docid = os.path.basename(_file.name)

        _file.close()

        words = separatewords(txt)

        articlewords.append({})
        articletitles.append(docid)

        # Increase the counts for this word in allwords and in articlewords
        for word in words:
            allwords.setdefault(word, 0)
            allwords[word] += 1
            articlewords[ec].setdefault(word, 0)
            articlewords[ec][word] += 1
        ec += 1
    return allwords, articlewords, articletitles


def makematrix(allw: list = None, articlew: list = None) -> (list, list):
    """Converting allwords and article_words to a matrix."""
    # wordvec = []

    # Only take words that are common but not too common
    # Because of text parsing on stopwords, this isn't needed.
    wordvec = [
        word for word, count in allw.items()
        if 3 < count < len(articlew) * 0.6
    ]
    # for word, count in allw.items():
    #     # if count > 3 and count < len(articlew) * 0.6:
    #     if 3 < count < len(articlew) * 0.6:
    #         wordvec.append(word)

    # Create and return the word matrix, along with the wordvec list.
    return [[(word in f and f[word] or 0)
             for word in wordvec] for f in articlew], wordvec


def add_to_matrix():
    """Adds rows (articles, documents) to a matrix."""

    pass


def remove_from_matrix():
    """Removes rows from a matrix."""
    pass


def showfeatures(w, h, titles, wordvec, out='features.txt'):
    outfile = open(out, 'w')
    pc, wc = numpy.shape(h)
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # Loop over all the features
    for i in range(pc):
        slist = []
        # Create a list of words and their weights
        for j in range(wc):
            slist.append((h[i, j], wordvec[j]))
        # Reverse sort the word list
        slist.sort()
        slist.reverse()

        # Print the first six elements
        n = [s[1] for s in slist[0:6]]
        outfile.write(str(n) + '\n')
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
        for f in flist[0:3]:
            outfile.write(str(f) + '\n')
        outfile.write('\n')

    outfile.close()
    # Return the pattern names for later use
    return toppatterns, patternnames


def showarticles(titles, toppatterns, patternnames, out='articles.txt'):
    """

    :param titles:
    :param toppatterns:
    :param patternnames:
    :param out:
    :return:
    """
    outfile = open(out, 'w')
    # Loop over all the articles
    for j in range(len(titles)):
        outfile.write(titles[j] + '\n')
        # Get the top features for this article and
        # reverse sort them
        toppatterns[j].sort()
        toppatterns[j].reverse()
        # Print the top three patterns
        for i in range(3):
            outfile.write(str(toppatterns[j][i][0]) + ' ' +
                          str(patternnames[toppatterns[j][i][1]]) + '\n')
        outfile.write('\n')
    outfile.close()


def circular_tree(weights: numpy.ndarray = None, feat: numpy.ndarray = None):
    """
    Rendering the circular tree
    :param feat:
    :param weights:
    :return:
    """
    set_corpus('/path/to/container')

    allwords, articlewords, articletitles = get_words()

    wordmatrix, wordvec = makematrix(allwords, articlewords)
    clust = clusters.hcluster(wordmatrix)

    # clusters.drawdendrogram(clust, articletitles, jpeg='wiki.jpg')
    clustjson, depth = clusters.hcluster_to_json(clust, labels=articletitles)

    v = numpy.ndarray(wordmatrix)

    topp, pn = showfeatures(weights, feat, articletitles, wordvec)
    showarticles(articletitles, topp, pn)

    return clustjson


def set_corpus(path):
    """Setting up the corpus path."""
    global CORPUSPATH
    corpus_path = os.path.normpath(os.path.abspath(path))
    if not os.path.isdir(corpus_path):
        raise ValueError(corpus_path)
    CORPUSPATH = corpus_path


