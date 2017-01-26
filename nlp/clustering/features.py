

import os
import re


CORPUSPATH = None


def separatewords(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


def get_words():
    """Getting the words from a given corpora."""
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0

    for item in os.listdir(CORPUSPATH):
        path = os.path.normpath(os.path.join(CORPUSPATH, item))
        txt = ''
        with open(path, 'r') as _file:
            txt = _file.read()
        title = txt.split('\n')[0]
        words = separatewords(txt)

        articlewords.append({})
        articletitles.append(title)

        # Increase the counts for this word in allwords and in articlewords
        for word in words:
            allwords.setdefault(word, 0)
            allwords[word] += 1
            articlewords[ec].setdefault(word, 0)
            articlewords[ec][word] += 1
        ec += 1
    return allwords, articlewords, articletitles


def makematrix(allw: list, articlew: list):
    """Converting the arrays to a matrix."""
    wordvec = []

    # Only take words that are common but not too common
    for word, count in allw.items():
        if count > 3 and count < len(articlew) * 0.6:
            wordvec.append(word)

    # Create the word matrix
    wordmatrix = [[(word in f and f[word] or 0)
                   for word in wordvec] for f in articlew]
    return wordmatrix, wordvec


def main():
    global CORPUSPATH
    _ = '/home/dominik/Desktop/wiki/wikipedia/'
    corpus_path = os.path.normpath(os.path.abspath(_))
    if not os.path.isdir(corpus_path):
        raise ValueError(corpus_path)
    CORPUSPATH = corpus_path
    allwords, articlewords, articletitles = get_words()

    return makematrix(allwords, articlewords)


if __name__ == "__main__":
    wordmatrix, wordvec = main()
    print(wordvec[0:10])
    print(wordmatrix[1][0:10])
