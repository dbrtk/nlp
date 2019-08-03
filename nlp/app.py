import os

from celery import Celery

from nlp.config import celeryconf

celery = Celery('nlp')

celery.config_from_object(celeryconf)
