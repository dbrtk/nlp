import json
import os
import shutil
import tempfile

from celery import shared_task
import requests

from .config import CORPUS_COMPUTE_CALLBACK, CORPUS_NLP_CALLBACK, DATA_ROOT

from .views import call_factorize, features_and_docs


@shared_task(bind=True)
def test_task(self, a, b):

    return a + b


@shared_task(bind=True)
def factorize_matrices(self,
                       corpusid: str = None,
                       feats: int = 10,
                       words: int = 6,
                       docs_per_feat: int = 0,
                       feats_per_doc: int = 3,
                       dir_id: str = None):

    local_path = os.path.join(DATA_ROOT, dir_id)
    out = {'corpusid': corpusid,
           'path': os.path.join(local_path, corpusid),
           'local_path': local_path,
           'feats': feats,
           'error': False,
           'dir_id': dir_id}
    try:
        call_factorize(
            path=os.path.join(local_path, corpusid),
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
    """Called after generating weight and feature matrices for a given feature
       number.
    """
    corpusid = res.get('corpusid')
    feats = res.get('feats')
    error = res.get('error')
    local_path = res.get('local_path')

    tmp_dir = tempfile.mkdtemp()

    archive_path = shutil.make_archive(
        os.path.join(tmp_dir, str(feats)),
        'zip',
        os.path.join(local_path, corpusid, 'matrix', 'wf'),
        str(feats)
    )
    shutil.rmtree(local_path)
    requests.post(
        CORPUS_NLP_CALLBACK,
        data={
            'payload': json.dumps({
                'corpusid': corpusid,
                'feats': feats,
                'error': True if error else False
            })
        },
        files={'file': open(archive_path, 'rb')}
    )
    shutil.rmtree(tmp_dir)


@shared_task(bind=True, time_limit=900)
def compute_matrices(self, **kwds):
    """Computing matrices"""
    features_and_docs(
        path=kwds['local_path'],
        feats=kwds.get('feats'),
        corpusid=kwds.get('corpusid'),
        words=kwds.get('words'),
        docs_per_feat=kwds.get('docs_per_feat'),
        feats_per_doc=kwds.get('feats_per_doc')
    )
    return kwds


@shared_task(bind=True)
def compute_matrices_callback(self, data):

    tmp_dir = tempfile.mkdtemp()
    data_dir = os.path.join(DATA_ROOT, data.get('unique_id'))
    requests.post(CORPUS_COMPUTE_CALLBACK, data={
        'corpusid': data.get('corpusid'),
        'feats': data.get('feats')
    }, files={
        'file': open(shutil.make_archive(
            os.path.join(tmp_dir, 'matrix'),
            'zip',
            os.path.join(data_dir, data.get('corpusid'), 'matrix')
        ), 'rb')
    })
    shutil.rmtree(tmp_dir)
    shutil.rmtree(data_dir)
