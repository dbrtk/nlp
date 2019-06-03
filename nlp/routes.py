
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

    # todo(): delete

    pass


@nlp_app.route('/features-docs/')
def get_features_and_docs():

    # todo(): delete

    params = json.loads(request.body)
    features, docs = features_and_docs(**params)
    return jsonify({
        'features': features,
        'docs': docs
    })


@nlp_app.route('/test-celery/')
def test_celery():

    res = task.test_task.apply_async(args=[1, 22345345]).get()

    return jsonify({'success': True, 'result': res})
