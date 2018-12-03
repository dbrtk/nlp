
import os

from django.conf import settings

# PROXIMITY_BOT_PROJ is specific to the local deployment of proximity-bot.
# todo(): delete in production
PROXIMITY_BOT_PROJ = settings.PROJECT_DIR


MAX_ITERATE = 100

# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"

# Defines whether proximity-bot with rmxbot are run on a remote server. If 
# set to True, proximity-bot should be accessed on a different machine
PROXIMITYBOT_IS_REMOTE = False

# PROXIMITYBOT_ENDPOINT = 'http://proximity-bot.net'
PROXIMITYBOT_ENDPOINT = 'http://localhost:8000'

CORPUS_ENDPOINT = '/'.join([PROXIMITYBOT_ENDPOINT, 'corpus'])

__CORPUS_NLP_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'nlp-callback'])
CORPUS_NLP_CALLBACK = '{}/'.format(__CORPUS_NLP_CALLBACK)

_CORPUS_COMPUTE_CALLBACK = '/'.join(
    s.strip('/') for s in [CORPUS_ENDPOINT, 'sync-matrices'])
CORPUS_COMPUTE_CALLBACK = '{}/'.format(_CORPUS_COMPUTE_CALLBACK)

CORPUS_LEMMA_WORDS_PATH = 'lemma-words'

# the place where nlp will store its temporary files; i.e. matrices, corpora.
DATA_ROOT = os.path.join(PROXIMITY_BOT_PROJ, 'data', 'nlp')

# nltk confiigs
# NLTK_DATA_PATH = '/opt/nltk_data'
NLTK_DATA_PATH = os.path.join(DATA_ROOT, 'nltk_data')
