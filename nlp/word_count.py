
import os
import re

import langdetect
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pycountry

from .config import DEFAULT_LANGUAGE


class TextFile(object):

    def __init__(self, path: str = None, detect_lang: bool = False,
                 allwords: dict = None):

        self.path = path
        self.txt = None
        self.language = None

        self.stem = None
        self.stopwords = None

        self.allwords = allwords

        self.info = {
            'stopwords': False,
            'language': None,
        }

    def __call__(self):

        with open(self.path, 'r') as _file:
            self.txt = _file.read()

        docid = self.txt.split('\n')[0]
        self.language = langdetect.detect(self.txt)

        lang = self.lang_name()

        self.info['language'] = lang

        try:
            self.stem = SnowballStemmer(lang, ignore_stopwords=True)
        except ValueError:
            pass

        try:
            self.stopwords = set(stopwords.words(lang))
            self.info['stopwords'] = True
        except OSError:
            self.stopwords = []

        return docid, self.process_txt(), self.info

    def lang_name(self):

        if len(self.language) != 2:
            raise RuntimeError(self.language)
        try:
            return pycountry.languages.get(alpha_2=self.language).name.lower()
        except Exception:
            return DEFAULT_LANGUAGE

    def process_txt(self):

        out = {}
        words = separatewords(self.txt)

        for word in words:
            if word in self.stopwords:
                continue

            if self.stem:
                word = self.stem.stem(word)

            out.setdefault(word, 0)
            out[word] += 1

            self.allwords.setdefault(word, 0)
            self.allwords[word] += 1
        return out


def separatewords(text):

    splitter = re.compile(r'\W*')
    return [s.lower() for s in splitter.split(text)]


class Corpus(object):

    def __init__(self, corpus: str = None):

        self.corpus_path = corpus

        self.allwords = {}
        self.articlewords = []
        self.articletitles = []
        self.info = []

    def __call__(self): self.iter_corpus()

    def iter_corpus(self):

        for file_name in os.listdir(self.corpus_path):

            inst = TextFile(
                path=os.path.normpath(
                    os.path.join(self.corpus_path, file_name)),
                allwords=self.allwords,
                detect_lang=True
            )
            docid, articlewords, info = inst()
            self.info.append(info)

            self.articletitles.append(docid)

            self.allwords = inst.allwords
            self.articlewords.append(articlewords)


def get_words(path):

    inst = Corpus(corpus=path)
    inst()
    return inst.allwords, inst.articlewords, inst.articletitles
