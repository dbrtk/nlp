
import os
import re

import numpy


CORPUSPATH = '/path/to/container'


def separatewords(text):
    # splitter = re.compile('\\W*')
    splitter = re.compile(r'\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


def get_words(corpus: str = None) -> (dict, list, list):
    """Getting the words from a given corpora."""
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0

    for item in os.listdir(corpus or CORPUSPATH):
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


def set_corpus(path):
    """Setting up the corpus path."""
    global CORPUSPATH
    corpus_path = os.path.normpath(os.path.abspath(path))
    if not os.path.isdir(corpus_path):
        raise ValueError(corpus_path)
    CORPUSPATH = corpus_path
