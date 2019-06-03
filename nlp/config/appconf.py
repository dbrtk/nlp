
import os


MAX_ITERATE = 100

# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"

# Defines whether proximity-bot with rmxbot are run on a remote server. If
# set to True, proximity-bot should be accessed on a different machine
PROXIMITYBOT_IS_REMOTE = False

# PROXIMITYBOT_ENDPOINT = 'http://proximity-bot.net'
PROXIMITYBOT_ENDPOINT = os.environ.get('PROXIMITYBOT_ENDPOINT')

CORPUS_ENDPOINT = '/'.join([PROXIMITYBOT_ENDPOINT, 'corpus'])

INTEGRITY_CHECK_CALLBACK = '{}/{}/'.format(
    CORPUS_ENDPOINT, 'integrity-check-callback')

CORPUS_LEMMA_WORDS_PATH = 'lemma-words'

# the place where nlp will store its temporary files; i.e. matrices, corpora.
DATA_ROOT = os.environ.get('DATA_ROOT')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

# nltk confiigs

NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH')

CELERY_TIME_LIMIT = 1800
