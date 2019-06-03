
import json
import os
import uuid

from flask import Blueprint, jsonify, request

from . import matrix_files, task
from .config.appconf import UPLOAD_FOLDER
from .views import features_and_docs

nlp_app = Blueprint('nlp_app', __name__, root_path='/')


def matrix_update():
    """Updating the matrices with new documents."""

    pass


@nlp_app.route('/features-docs/')
def get_features_and_docs():

    params = json.loads(request.body)
    features, docs = features_and_docs(**params)
    return jsonify({
        'features': features,
        'docs': docs
    })


@nlp_app.route('/integrity-check/', methods=['POST', 'GET'])
def integrity_check():
    """ The integrity check.
    :param request:
    :return:
    """
    params = json.loads(request.data)

    unique_id = uuid.uuid4().hex
    file = request.files['file']
    tmp_path = os.path.join(
        matrix_files.unpack_corpus(
            os.path.join(UPLOAD_FOLDER, file.filename),
            # request.files['file'].temporary_file_path(),
            unique_id=unique_id)
    )
    params['path'] = os.path.join(tmp_path, params.get('corpusid'))
    params['tmp_path'] = tmp_path

    task.integrity_check.apply_async(
        kwargs=params, link=task.integrity_check_callback.s())
    return jsonify({'success': True})


@nlp_app.route('/features-to-json/')
def features_to_json():

    pass


def dendogram():

    pass


def features_docs():

    pass


def features_count():

    pass


def remove_feature():

    pass


@nlp_app.route('/test-celery/')
def test_celery():

    res = task.test_task.apply_async(args=[1, 22345345]).get()

    return jsonify({'success': True, 'result': res})
