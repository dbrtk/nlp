
import json

from flask import Blueprint, jsonify, request

from .views import features_and_docs

nlp_app = Blueprint('nlp_app', __name__, root_path='/')


@nlp_app.route('/features-docs/')
def get_features_and_docs():

    # todo(): delete

    params = json.loads(request.body)
    features, docs = features_and_docs(**params)
    return jsonify({
        'features': features,
        'docs': docs
    })
