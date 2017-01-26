
import argparse
import os
import shutil

from nltk.corpus import PlaintextCorpusReader

from .tags import pos_tags_txt

BUFFSIZE = 8 * 1024
PATH = None
TAGGED_PATH = None


def make_path(string):
    """Validating the path to the corpus."""
    string = os.path.abspath(string)
    if not os.path.isdir(string):
        raise ValueError(string)
    return os.path.normpath(string)


def text_corpus():
    return PlaintextCorpusReader(PATH, '.*')


def make_tagged_corpus_dir():
    global TAGGED_PATH
    corpus_name = 'tagged_%s' % os.path.basename(PATH)
    tagged_dir = os.path.join(os.path.dirname(PATH), corpus_name)
    if os.path.exists(tagged_dir):
        # raise ValueError(tagged_dir)
        shutil.rmtree(tagged_dir)
    os.mkdir(tagged_dir)
    TAGGED_PATH = tagged_dir
    if not os.path.isdir(TAGGED_PATH):
        raise RuntimeError(TAGGED_PATH)


def tag_doc(fileid, _path, tagged_dir=None):
    """Copying the content of a file, tagging it and saving in a new file with
       the same name in the tagged corpus.
    """
    tagged_dir = TAGGED_PATH if TAGGED_PATH else tagged_dir    
    with open(_path, 'r') as corpus_file:
        with open(os.path.join(tagged_dir, fileid), 'w+') as tagged_corpus:
            for _line in corpus_file.readlines():
                if _line.strip():
                    tagged_corpus.write(pos_tags_txt(_line))
                tagged_corpus.write('\n')


def process_corpus(corpus):
    """Processing the corpus."""
    for item in corpus.fileids():
        _path = os.path.join(PATH, item)
        tag_doc(item, _path)


def main(_path):
    global PATH
    PATH = os.path.normpath(make_path(_path))
    make_tagged_corpus_dir()

    
def tag_corpus(_):
    """tagging all documents in a given corpus."""
    main(_)
    corpus_reader = text_corpus()
    for item in corpus_reader.fileids():
        _path = os.path.join(PATH, item)
        yield (item, _path, TAGGED_PATH)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Arguments including the path.')
    parser.add_argument('path', type=make_path)
    args = parser.parse_args()
    _path = args.path
    main(_path)
    process_corpus(text_corpus())
