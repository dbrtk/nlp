
import json
import os
import uuid

from flask import Blueprint, jsonify, request

from . import matrix_files, task
from .views import features_and_docs

nlp_app = Blueprint('nlp_app', __name__, root_path='/')


@nlp_app.route('/compute-matrices/', methods=['POST'])
def compute_matrices():
    """Computing matrices and generating features/weights for a given feature
       number.
    """

    # params = json.loads(request.POST.get('params'))

    params = request.get_json().get('params')
    unique_id = uuid.uuid4().hex
    params['local_path'] = os.path.join(
        matrix_files.unpack_corpus(
            request.FILES['file'].temporary_file_path(),
            unique_id=unique_id),
        params.get('corpusid'))

    params['unique_id'] = unique_id
    task.compute_matrices.apply_async(
        kwargs=params,
        link=task.compute_matrices_callback.s())
    return jsonify({'success': True})


def matrix_update():
    """Updating the matrices with new documents."""

    pass


@nlp_app.route('/generate-features-weights/')
def generate_features_weights():

    # params = json.loads(request.POST.dict().get('payload'))
    params = request.get_json()

    unique_id = uuid.uuid4().hex
    params['dir_id'] = unique_id

    matrix_files.unpack_vectors(
        request.FILES['file'].temporary_file_path(),
        unique_id=unique_id)

    task.factorize_matrices.apply_async(
        kwargs=params,
        link=task.gen_matrices_callback.s())
    return jsonify({'success': True})


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
    params = request.get_json()
    unique_id = uuid.uuid4().hex
    tmp_path = os.path.join(
        matrix_files.unpack_corpus(
            request.files['file'].temporary_file_path(),
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
