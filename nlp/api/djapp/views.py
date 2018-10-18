

import json
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ... import task
from ...views import features_and_docs



@csrf_exempt
def compute_matrices(request):
    """Computing matrices and generating features/weights for a given feature
       number.
    """
    params = json.loads(request.body)
    
    task.compute_matrices.apply_async(
        kwargs=params,
        link=task.compute_matrices_callback.s())
    return JsonResponse({'success': True})


@csrf_exempt
def generate_features_weights(request):

    params = json.loads(request.POST.dict().get('payload'))
    corpusid = params.get('corpus_id')

    dir_id = uuid.uuid4().hex
    params['dir_id'] = dir_id

    task.factorize_matrices.apply_async(
        kwargs=params,
        link=task.gen_matrices_callback.s())
    return JsonResponse({'success': True})


def get_features_and_docs(request):

    params = json.loads(request.body)
    features, docs = features_and_docs(**params)

    return JsonResponse({
        'features': features,
        'docs': docs
    })


def features_to_json(request):

    pass


def dendogram(request):

    pass


def features_docs(request):

    pass


def features_count(request):

    pass


def remove_feature(request):

    pass


def test_celery(request):

    res = task.test_task.apply_async(args=[1, 22345345]).get()

    return JsonResponse({'success': True, 'result': res})
