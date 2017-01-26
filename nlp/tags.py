
from nltk import pos_tag, word_tokenize
from nltk.tag.util import tuple2str


def pos_tags_txt(string):
    """Tokenizing and posing tags on text."""

    return ' '.join(
        [tuple2str(_) for _ in
         pos_tag(
             word_tokenize(string)
        )]
    )
