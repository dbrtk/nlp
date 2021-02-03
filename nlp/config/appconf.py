
import os

# nltk confiigs
NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH')

DATA_FOLDER = os.environ.get('DATA_FOLDER')

# celery configs
CELERY_TIME_LIMIT = 1800

TEXT_FOLDER = 'text'

MATRIX_FOLDER = 'matrix'

# settings for the endpoint that implements non-negative matrix factorization
NMF_ENDPOINT = os.environ.get('NMF_ENDPOINT')

# RabbitMQ configuration
# RabbitMQ rpc queue name
# These values are defined on the level of docker-compose.
RPC_QUEUE_NAME = os.environ.get('RPC_QUEUE_NAME', 'nlp')

# login credentials for RabbitMQ.
RPC_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RPC_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RPC_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')

# the host to which the rpc broker (rabbitmq) is deployed
RPC_HOST = os.environ.get('RABBITMQ_HOST')
RPC_PORT = os.environ.get('RABBITMQ_PORT', 5672)


# REDIS CONFIG
# celery, redis (auth access) configuration
BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER')
REDIS_PORT = os.environ.get('REDIS_PORT')
