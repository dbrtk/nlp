import os

from celery import Celery

from nlp.config import celeryconf

# UPLOAD_FOLDER = os.path.expanduser('~/Data/tmp')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ['PROXIMITYBOT_ENDPOINT'] = 'http://localhost:8000'

# os.environ['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['NLTK_DATA_PATH'] = os.path.expanduser('~/Data/nltk_data')



celery = Celery('nlp')
celery.config_from_object(celeryconf)

