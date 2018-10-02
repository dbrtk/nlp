import os

MAX_ITERATE = 100


# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"


PROXIMITY_BOT_HOSTNAME = 'localhost:5000'

# PROXIMITY_BOT_HOST = 'http://proximity-bot.net'
PROXIMITY_BOT_HOST = 'localhost:5000'

# PROXIMITY_USER = 'queeliot'
PROXIMITY_USER = 'dominik'

CORPUS_ENDPOINT = '/'.join([PROXIMITY_BOT_HOST, 'corpus'])

__CORPUS_NLP_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'nlp-callback'])
CORPUS_NLP_CALLBACK = '{}/'.format(__CORPUS_NLP_CALLBACK)

_CORPUS_COMPUTE_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'compute-matrices-callback'])
CORPUS_COMPUTE_CALLBACK = '{}/'.format(_CORPUS_COMPUTE_CALLBACK)

CORPUS_LEMMA_WORDS_PATH = 'lemma-words'


DATA_ROOT = os.path.abspath('/data')


RSYNC_SCRIPTS_PATH = os.path.abspath('/opt/rmxbin')
RSYNC_GET_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'getdata.sh')
RSYNC_GET_VECTORS = os.path.join(RSYNC_SCRIPTS_PATH, 'getvect.sh')
RSYNC_POST_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'postdata.sh')


# nltk confiigs
NLTK_DATA_PATH = '/opt/nltk_data'
