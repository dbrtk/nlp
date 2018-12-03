import os

from django.conf import settings

# PROXIMITY_BOT_PROJ is specific to the local deployment of proximity-bot.
PROXIMITY_BOT_PROJ = settings.PROJECT_DIR

MAX_ITERATE = 100

# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"

PROXIMITYBOT_IS_REMOTE = True

# proximity-bot host name is used within scripts that use rsync or scp/ssh.
PROXIMITYBOT_HOST_NAME = 'rmxbotweb:8000'

# PROXIMITYBOT_ENDPOINT = 'http://proximity-bot.net'
PROXIMITYBOT_ENDPOINT = 'http://rmxbotweb:8000'

PROXIMITY_USER = 'rmxbotuser'

CORPUS_ENDPOINT = '/'.join([PROXIMITYBOT_ENDPOINT, 'corpus'])

__CORPUS_NLP_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'nlp-callback'])
CORPUS_NLP_CALLBACK = '{}/'.format(__CORPUS_NLP_CALLBACK)

_CORPUS_COMPUTE_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'compute-matrices-callback'])
CORPUS_COMPUTE_CALLBACK = '{}/'.format(_CORPUS_COMPUTE_CALLBACK)

CORPUS_LEMMA_WORDS_PATH = 'lemma-words'

# the place where nlp will store its temporary files; i.e. matrices, corpora.
DATA_ROOT = '/data/nlpdata'


# RSYNC_SCRIPTS_PATH = os.path.abspath('/opt/rmxbin')
# These are small shell scripts from rmxbin.
RSYNC_SCRIPTS_PATH = os.path.abspath('/opt/rmxbin')

RSYNC_GET_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'getdata.sh')
RSYNC_GET_VECTORS = os.path.join(RSYNC_SCRIPTS_PATH, 'getvect.sh')
RSYNC_POST_DATA = os.path.join(RSYNC_SCRIPTS_PATH, 'postdata.sh')

# __LOCAL_REMOTE = 'remote' if PROXIMITYBOT_IS_REMOTE else 'local'

# RSYNC_GET_DATA = os.path.join(RSYNC_SCRIPTS_PATH, __LOCAL_REMOTE, 'getdata.sh')
# RSYNC_GET_VECTORS = os.path.join(
#     RSYNC_SCRIPTS_PATH, __LOCAL_REMOTE, 'getvect.sh')
# RSYNC_POST_DATA = os.path.join(
#     RSYNC_SCRIPTS_PATH, __LOCAL_REMOTE, 'postdata.sh')


# nltk confiigs
# NLTK_DATA_PATH = '/opt/nltk_data'
NLTK_DATA_PATH = '/data/nltk_data'