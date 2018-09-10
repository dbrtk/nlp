import os

MAX_ITERATE = 100


# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"


PROXIMITY_BOT_HOST = 'http://proximity-bot.net'
PROXIMITY_USER = 'queeliot'

CORPUS_ENDPOINT = '/'.join([PROXIMITY_BOT_HOST, 'corpus'])

__CORPUS_NLP_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'nlp-callback'])
CORPUS_NLP_CALLBACK = '{}/'.format(__CORPUS_NLP_CALLBACK)

_CORPUS_COMPUTE_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'compute-matrices-callback'])
CORPUS_COMPUTE_CALLBACK = '{}/'.format(_CORPUS_COMPUTE_CALLBACK)

CORPUS_LEMMA_WORDS_PATH = 'lemma-words'


DATA_ROOT = os.path.abspath('/home/dominik/www/nlp')


RSYNC_SCRIPTS_PATH = os.path.abspath('/home/dominik/Projects/rmxbin')
RSYNC_GET_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'getdata.sh')
RSYNC_POST_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'postdata.sh')
