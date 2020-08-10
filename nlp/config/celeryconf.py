
from .appconf import BROKER_HOST_NAME, REDIS_PASS


_url = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:6379/0'

BROKER_URL = _url
CELERY_RESULT_BACKEND = _url

CELERY_IMPORTS = ('nlp.task', )

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ROUTES = {

    'nlp.task.*': {'queue': 'nlp'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},

    'rmxnmf.task.*': {'queue': 'rmxnmf'},
}

RMXBOT_TASKS = {

    'nlp_callback': 'rmxbot.tasks.container.nlp_callback_success',

    'integrity_check_callback': 'rmxbot.tasks.container.integrity_check_callback',

}

RMXNMF_TASKS = {

    'factorize_matrix': 'rmxnmf.task.factorize_matrix'

}

