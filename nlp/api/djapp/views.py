

import json
import os
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy

from ... import config, task
from ...data import CorpusMatrix
from ...views import features_and_docs


def handle_uploaded_file(path, binary_file, dtype, shape):

    dtype = numpy.dtype(dtype)

    numpy.save(path, numpy.fromfile(binary_file, dtype=dtype).reshape(shape))

    if not os.path.isfile('%s.npy' % path):
        raise RuntimeError('%s.npy' % path)
    return '%s.npy' % path


@csrf_exempt
def compute_matrices(request):

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

    path = os.path.join(config.DATA_ROOT, dir_id)
    inst = CorpusMatrix(
        path=path, featcount=params.get('feats'), corpusid=corpusid)

    file_path = handle_uploaded_file(
        inst.file_path('vectors'),
        request.FILES['file'],
        params.pop('dtype'),
        params.pop('shape'))

    inst.chmod_fd(file_path)

    params['path'] = path
    params['dir_id'] = dir_id

    task.factorize_matrices.apply_async(
        kwargs=params,
        link=task.gen_matrices_callback.s())
    return JsonResponse({'success': True})


def get_features_and_docs(request):

    params = json.loads(request.body)

    print('get_features_and_docs')
    print(params)

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

    print('test the celery task!')
    print(request)
    print(task.test_task)
    print(task.test_task.delay)

    res = task.test_task.apply_async(args=[1, 22345345]).get()

    return JsonResponse({'success': True, 'result': res})
