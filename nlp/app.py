import os

from celery import Celery
from flask import Flask
from werkzeug.routing import BaseConverter

from nlp.config import celeryconf

UPLOAD_FOLDER = os.path.expanduser('~/Data/tmp')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'data')

print(BASE_DIR)
print(DATA_ROOT)

os.environ['PROXIMITYBOT_ENDPOINT'] = 'http://localhost:8000'
# os.environ['DATA_ROOT'] = os.path.expanduser('~/Data/nlp')
os.environ['DATA_ROOT'] = DATA_ROOT
os.environ['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.environ['NLTK_DATA_PATH'] = os.path.expanduser('~/Data/nltk_data')


class ObjectidConverter(BaseConverter):
    """A url converter for bson's ObjectId."""

    regex = r"[a-f0-9]{24}"


def create_app():
    """Building up the flask applicaiton."""
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.url_map.converters['objectid'] = ObjectidConverter

    with app.app_context():
        from .routes import nlp_app

        app.register_blueprint(nlp_app)

    return app


celery = Celery('nlp')
celery.config_from_object(celeryconf)

