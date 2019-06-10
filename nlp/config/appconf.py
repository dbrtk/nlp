
import os


MAX_ITERATE = 100

# language processing (detection)
DEFAULT_LANGUAGE = 'english'

STOPWORD_REPLACEMENT = "___"

# the place where nlp will store its temporary files; i.e. matrices, corpora.
DATA_ROOT = os.environ.get('DATA_ROOT')

REDIS_HOST_NAME = os.environ.get('REDIS_HOST_NAME')

# nltk confiigs
NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH')

# celery configs
CELERY_TIME_LIMIT = 1800

