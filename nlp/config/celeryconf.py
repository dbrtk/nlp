

from .appconf import RPC_HOST, RPC_PASS, RPC_PORT, RPC_USER, RPC_VHOST

# redis config imports
from .appconf import BROKER_HOST_NAME, REDIS_DB_NUMBER, REDIS_PASS, REDIS_PORT


# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
_url = f'amqp://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}/{RPC_VHOST}'


broker_url = _url

# result_backend = "rpc://"

# redis result backend
result_backend = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:{REDIS_PORT}/{REDIS_DB_NUMBER}'

result_persistent = True

imports = ('nlp.task', )

result_expires = 30
timezone = 'UTC'

accept_content = ['json', 'msgpack', 'yaml']
task_serializer = 'json'
result_serializer = 'json'

task_routes = {

    'nlp.task.*': {'queue': 'nlp'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},

    'rmxnmf.task.*': {'queue': 'rmxnmf'},
}

RMXWEB_TASKS = {

    'nlp_callback': 'rmxbot.tasks.container.nlp_callback_success',

    'integrity_check_callback': 'rmxbot.tasks.container.integrity_check_callback',

}

RMXNMF_TASKS = {

    'factorize_matrix': 'rmxnmf.task.factorize_matrix'

}

