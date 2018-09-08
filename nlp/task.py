import json
import os
import shlex
import shutil
import subprocess
import uuid

from celery import shared_task
import requests

from .config import CORPUS_COMPUTE_CALLBACK, CORPUS_NLP_CALLBACK
from .matrix_files import sync_corpus_data
from .views import call_factorize, features_and_docs


@shared_task(bind=True)
def test_task(self, a, b):

    return a + b


@shared_task(bind=True)
def generate_matrices(self,
                      corpusid: str = None,
                      path: str = None,
                      feats: int = 10,
                      words: int = 6,
                      docs_per_feat: int = 0,
                      feats_per_doc: int = 3):

    # todo(): implement the rsync-get matrices before computing.

    # path = self.get_corpus_path()

    out = {'corpusid': corpusid, 'path': path, 'feats': feats, 'error': False}
    try:
        features_and_docs(
            path=path,
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
def factorize_matrices(self,
                       corpusid: str = None,
                       path: str = None,
                       feats: int = 10,
                       words: int = 6,
                       docs_per_feat: int = 0,
                       feats_per_doc: int = 3,
                       dir_id: str = None):

    out = {'corpusid': corpusid,
           'path': path,
           'feats': feats,
           'error': False,
           'dir_id': dir_id}
    try:
        call_factorize(
            path=path,
            feats=feats,
            corpusid=corpusid,
            words=words,
            docs_per_feat=docs_per_feat,
            feats_per_doc=feats_per_doc
        )
    except (IndexError, Exception,) as err:
        raise
        out['error'] = True
        return out
    return out


@shared_task(bind=True)
def gen_matrices_callback(self, res):

    corpusid = res.get('corpusid')
    path = res.get('path')
    feats = res.get('feats')
    error = res.get('error')

    _path = os.path.join(path, 'matrix', 'wf', str(feats))

    command = 'tar -zcvf %(path)s.tar.gz -C %(path)s .' % {'path': _path}

    res = subprocess.run(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    requests.post(CORPUS_NLP_CALLBACK, data={
        'payload': json.dumps({
            'corpusid': corpusid,
            'feats': feats,
            'error': True if error else False,
            'path': path
        })}, files={'file': open('%s.tar.gz' % (_path), 'rb')})

    shutil.rmtree(path)


@shared_task(bind=True)
def compute_matrices(self, **kwds):

    unique_id = uuid.uuid4().hex
    kwds['unique_id'] = unique_id
    local_path = sync_corpus_data(corpusid=kwds.get('corpusid'),
                                  unique_id=unique_id,
                                  remote_path=kwds.get('path'))

    features_and_docs(
        path=local_path,
        feats=kwds.get('feats'),
        corpusid=kwds.get('corpusid'),
        words=kwds.get('words'),
        docs_per_feat=kwds.get('docs_per_feat'),
        feats_per_doc=kwds.get('feats_per_doc')
    )
    kwds['local_path'] = local_path

    local_path = sync_corpus_data(
        unique_id=unique_id,
        corpusid=kwds.get('corpusid'),
        remote_path=kwds.get('path'),
        get=False)

    return kwds


@shared_task(bind=True)
def compute_matrices_callback(self, data):

    shutil.rmtree(data.get('local_path'))

    requests.post(CORPUS_COMPUTE_CALLBACK, json={
        'corpusid': data.get('corpusid'),
        'feats': data.get('feats'),
        'path': data.get('path')
    })
