
import os
import re
import pprint

import numpy

from . import clusters
from . import nmf

CORPUSPATH = None
PRINTER = pprint.PrettyPrinter(indent=4)


def separatewords(text):
    # splitter = re.compile('\\W*')
    splitter = re.compile(r'\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


def get_words(corpus: str = None):
    """Getting the words from a given corpora."""
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0

    for item in os.listdir(corpus or CORPUSPATH):
        path = os.path.normpath(os.path.join(CORPUSPATH, item))
        txt = ''
        with open(path, 'r') as _file:
            txt = _file.read()
        docid = txt.split('\n')[0]
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


def makematrix(allw: list = None, articlew: list = None):
    """Converting the arrays to a matrix."""
    wordvec = []

    # Only take words that are common but not too common
    # Because of text parsing on stopwords, this isn't needed.
    for word, count in allw.items():
        if count > 3 and count < len(articlew) * 0.6:
            wordvec.append(word)

    # Create the word matrix
    wordmatrix = [[(word in f and f[word] or 0)
                   for word in wordvec] for f in articlew]
    return wordmatrix, wordvec


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


def circular_tree(path_to_data):
    set_corpus('/home/dominik/Desktop/wiki/tiny/')

    allwords, articlewords, articletitles = get_words()

    wordmatrix, wordvec = makematrix(allwords, articlewords)
    clust = clusters.hcluster(wordmatrix)

    # clusters.drawdendrogram(clust, articletitles, jpeg='wiki.jpg')
    clustjson, depth = clusters.hcluster_to_json(clust, labels=articletitles)

    v = numpy.matrix(wordmatrix)

    weights, feat = nmf.factorize(v, pc=20, iter=50)

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


def main():
    # _ = '/home/dominik/Desktop/wiki/wikipedia/'
    _ = '/home/dominik/Desktop/wiki/tiny/'

    set_corpus(_)
    allwords, articlewords, articletitles = get_words()

    wordmatrix, wordvec = makematrix(allwords, articlewords)

    # clust = clusters.hcluster(wordmatrix)
    # clustjson, depth = clusters.hcluster_to_json(clust, labels=articletitles)

    v = numpy.matrix(wordmatrix)
    print(v)
    weights, feat = nmf.factorize(v, pc=20, iter=100)

    print(feat)
    print(weights)

    topp, pn = showfeatures(weights, feat, articletitles, wordvec)

    showarticles(articletitles, topp, pn)


if __name__ == "__main__":
    main()
