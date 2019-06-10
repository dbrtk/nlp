import os

from celery import Celery

from nlp.config import celeryconf

UPLOAD_FOLDER = os.path.expanduser('~/Data/tmp')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'data')

os.environ['PROXIMITYBOT_ENDPOINT'] = 'http://localhost:8000'
os.environ['DATA_ROOT'] = DATA_ROOT
os.environ['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.environ['NLTK_DATA_PATH'] = os.path.expanduser('~/Data/nltk_data')



celery = Celery('nlp')
celery.config_from_object(celeryconf)

