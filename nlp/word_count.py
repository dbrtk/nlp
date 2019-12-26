import os
import re

import langdetect
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import pycountry

from .config.appconf import NLTK_DATA_PATH

nltk.data.path.append(NLTK_DATA_PATH)
del nltk


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
    """Procesisng the text file; lemmatizing."""
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
            docid = os.path.basename(_file.name)

        try:
            self.language = langdetect.detect(self.txt)
            lang = self.lang_name()
            self.info['language'] = lang

        # except langdetect.lang_detect_exception.LangDetectException as err:
        except langdetect.detector_factory.LangDetectException as err:
            del err
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
            return None

        if word in self.stopwords:
            return None

        if not re.match(r'^\w*$', word):
            return None

        return word.lower()

    def lemmatize_txt(self):

        out = {}

        for word, _ in pos_tag(word_tokenize(self.txt)):

            word = self.process_word(word)
            if word is None or not word:
                continue

            pos = get_wordnet_pos(_)
            if not pos:
                continue

            lemma = self.lem.lemmatize(word, pos=pos)

            out.setdefault(lemma, 0)
            out[lemma] += 1

            self.lemma_word.setdefault(lemma, [])
            if word not in self.lemma_word[lemma]:
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
    """Processing a corpus."""
    def __init__(self,
                 corpus_path: str = None,
                 allwords: dict = None,
                 articlewords: list = None,
                 articletitles: [] = None,
                 lemma_words: list = None,
                 added_texts: list = None,
                 removed_texts: list = None):

        self.corpus_path = corpus_path

        self.added_texts = added_texts
        self.removed_texts = removed_texts

        self.allwords = allwords or {}
        self.articlewords = articlewords or []
        self.articletitles = articletitles or []
        self.info = []

        self.lemma_word = lemma_words or {}

    def __call__(self): self.iter_corpus()

    def iter_corpus(self):

        if self.added_texts:
            files = self.added_texts
        else:
            files = os.listdir(self.corpus_path)

        for file_name in files:

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


class RemoveTexts(object):

    pass


def process_lemma_word(obj):

    for lemma, words in obj.items():
        if len(words) == 1 and words[0] == lemma:
            continue
        yield {'lemma': lemma, 'words': words}


def get_words(path):
    """Generating the word count and lemma."""
    inst = CorpusDir(corpus_path=path)
    inst()

    lemma_word = list(process_lemma_word(inst.lemma_word))

    return inst.allwords, inst.articlewords, inst.articletitles, lemma_word
