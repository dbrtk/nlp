
import os


MAX_ITERATE = 100

# language processing (detection)
DEFAULT_LANGUAGE = 'english'

REDIS_HOST_NAME = os.environ.get('REDIS_HOST_NAME')

# nltk confiigs
NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH')

# celery configs
CELERY_TIME_LIMIT = 1800

TEXT_FOLDER = 'text'
MATRIX_FOLDER = 'matrix'