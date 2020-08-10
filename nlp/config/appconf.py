
import os

BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')

# nltk confiigs
NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH')

DATA_FOLDER = os.environ.get('DATA_FOLDER')

# celery configs
CELERY_TIME_LIMIT = 1800

TEXT_FOLDER = 'text'

MATRIX_FOLDER = 'matrix'

# settings for the endpoint that implements non-negative matrix factorization
NMF_ENDPOINT = os.environ.get('NMF_ENDPOINT')

# celery, redis (auth access) configuration
REDIS_PASS = os.environ.get('REDIS_PASS')
