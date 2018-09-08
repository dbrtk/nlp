import json
import os
import re

import langdetect
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import pycountry
import requests

from .config import (
    CORPUS_ENDPOINT, CORPUS_LEMMA_WORDS_PATH, STOPWORD_REPLACEMENT)


def get_wordnet_pos(treebank_tag):
    """ Given a treebank tag, returns a wordnet tag. """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


class TextFile(object):

    def __init__(self, path: str = None, detect_lang: bool = False,
                 allwords: dict = None, lemma_word: dict = None):

        self.path = path
        self.txt = None
        self.language = None

        self.stem = None
        self.stopwords = []
        self.lem = None

        self.allwords = allwords

        self.info = {
            'stopwords': False,
            'language': None,
        }

        self.lemma_word = lemma_word if lemma_word else {}

    def __call__(self, stemming: bool = False):

        with open(self.path, 'r') as _file:
            self.txt = _file.read()

        docid = self.txt.split('\n')[0]
        try:
            self.language = langdetect.detect(self.txt)
            lang = self.lang_name()
            self.info['language'] = lang

        except langdetect.lang_detect_exception.LangDetectException as err:

            # lang detect is not able to detect the language; the support may
            # be missing.
            pass
        else:
            self.set_lem()

            if stemming:
                self.set_stem(lang)

            self.set_stopwords(lang)

        if self.lem:
            # this is only executed when a lemmatizer is defined on self.lem
            return docid, self.lemmatize_txt(), self.info
        return docid, self.process_txt(), self.info

    def set_stem(self, lang):

        try:
            self.stem = SnowballStemmer(lang, ignore_stopwords=True)
        except ValueError:
            pass

    def set_lem(self):

        if self.language in ['en']:
            self.lem = WordNetLemmatizer()

    def set_stopwords(self, lang):

        try:
            self.stopwords = set(stopwords.words(lang))
            self.info['stopwords'] = True
        except OSError:
            self.stopwords = set()

    def lang_name(self):

        try:
            return pycountry.languages.get(alpha_2=self.language).name.lower()
        except Exception:
            return ''

    def process_word(self, word):

        if len(word) < 3:
            return STOPWORD_REPLACEMENT

        if word in self.stopwords:
            return STOPWORD_REPLACEMENT

        if not re.match(r'^\w*$', word):
            return STOPWORD_REPLACEMENT

        return word.lower()

    def lemmatize_txt(self):

        out = {}

        for word, _ in pos_tag(word_tokenize(self.txt)):

            word = self.process_word(word)

            # todo(): implement a better way of handling stopwords
            # todo(): review the line below
            if word == STOPWORD_REPLACEMENT:
                continue

            pos = get_wordnet_pos(_)
            if not pos:
                continue

            lemma = self.lem.lemmatize(word, pos=pos)

            out.setdefault(lemma, 0)
            out[lemma] += 1

            self.lemma_word.setdefault(lemma, [])
            if not word in self.lemma_word[lemma]:
                self.lemma_word[lemma].append(word)

            self.allwords.setdefault(lemma, 0)
            self.allwords[lemma] += 1

        return out

    def process_txt(self):

        out = {}
        words = separatewords(self.txt)

        for word in words:

            word = self.process_word(word)

            if self.stem:
                word = self.stem.stem(word)

            out.setdefault(word, 0)
            out[word] += 1

            self.allwords.setdefault(word, 0)
            self.allwords[word] += 1
        return out


def separatewords(text):

    splitter = re.compile(r'\W+')
    return [s.lower() for s in splitter.split(text)]


class CorpusDir(object):

    def __init__(self, corpus: str = None):

        self.corpus_path = corpus

        self.allwords = {}
        self.articlewords = []
        self.articletitles = []
        self.info = []

        self.lemma_word = {}

    def __call__(self): self.iter_corpus()

    def iter_corpus(self):

        for file_name in os.listdir(self.corpus_path):

            inst = TextFile(
                path=os.path.normpath(
                    os.path.join(self.corpus_path, file_name)),
                allwords=self.allwords,
                detect_lang=True,
                lemma_word=self.lemma_word
            )
            docid, articlewords, info = inst()

            self.lemma_word = inst.lemma_word
            self.info.append(info)

            self.articletitles.append(docid)

            self.allwords = inst.allwords
            self.articlewords.append(articlewords)


def process_lemma_word(obj):

    for lemma, words in obj.items():
        if len(words) == 1 and words[0] == lemma:
            continue
        yield {'lemma': lemma, 'words': words}


def get_words(path, corpusid: str = None):

    inst = CorpusDir(corpus=path)
    inst()

    lemma_word = list(process_lemma_word(inst.lemma_word))

    return inst.allwords, inst.articlewords, inst.articletitles, lemma_word
