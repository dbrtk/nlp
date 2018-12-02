import json
import os
import uuid

from celery import shared_task
import requests

from .config import CORPUS_COMPUTE_CALLBACK, CORPUS_NLP_CALLBACK, DATA_ROOT

from .matrix_files import sync_corpus_data
from .views import call_factorize, features_and_docs


@shared_task(bind=True)
def test_task(self, a, b):

    return a + b


@shared_task(bind=True)
def factorize_matrices(self,
                       corpusid: str = None,
                       path: str = None,
                       feats: int = 10,
                       words: int = 6,
                       docs_per_feat: int = 0,
                       feats_per_doc: int = 3,
                       dir_id: str = None):

    local_path = os.path.join(DATA_ROOT, dir_id)

    out = {'corpusid': corpusid,
           'path': path,
           'local_path': local_path,
           'feats': feats,
           'error': False,
           'dir_id': dir_id}

    sync_corpus_data(
        unique_id=dir_id,
        corpusid=corpusid,
        remote_path=path,
        get=False,
        get_vectors=True)

    try:
        call_factorize(
            path=local_path,
            feats=feats,
            corpusid=corpusid,
            words=words,
            docs_per_feat=docs_per_feat,
            feats_per_doc=feats_per_doc
        )
    except (IndexError, Exception,) as err:
        out['error'] = True
        return out
    return out


@shared_task(bind=True)
def gen_matrices_callback(self, res):

    corpusid = res.get('corpusid')
    path = res.get('path')
    feats = res.get('feats')
    error = res.get('error')
    local_path = res.get('local_path')
    dir_id = res.get('dir_id')

    os.remove(os.path.join(local_path, 'matrix', 'vectors.npy'))

    sync_corpus_data(
        unique_id=dir_id,
        corpusid=corpusid,
        remote_path=path,
        get=False)

    requests.post(CORPUS_NLP_CALLBACK, data={
        'payload': json.dumps({
            'corpusid': corpusid,
            'feats': feats,
            'error': True if error else False,
            'path': path
        })})


@shared_task(bind=True, time_limit=900)
def compute_matrices(self, **kwds):

    unique_id = kwds['unique_id']

    features_and_docs(
        path=kwds['local_path'],
        feats=kwds.get('feats'),
        corpusid=kwds.get('corpusid'),
        words=kwds.get('words'),
        docs_per_feat=kwds.get('docs_per_feat'),
        feats_per_doc=kwds.get('feats_per_doc')
    )
    # sync_corpus_data(
    #     unique_id=unique_id,
    #     # corpusid=kwds.get('corpusid'),
    #     remote_path=kwds.get('path'),
    #     get=False)

    return kwds


@shared_task(bind=True)
def compute_matrices_callback(self, data):

    requests.post(CORPUS_COMPUTE_CALLBACK, json={
        'corpusid': data.get('corpusid'),
        'feats': data.get('feats'),
        'path': data.get('path')
    })
