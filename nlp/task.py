import json
import os
import shutil

import requests

from.app import celery
from .config.appconf import CELERY_TIME_LIMIT, INTEGRITY_CHECK_CALLBACK
from .config.celeryconf import RMXBOT_TASKS
from .integrity_check import IntegrityCheck
from .views import call_factorize, features_and_docs


@celery.task
def test_task(a, b):

    return a + b


@celery.task
def factorize_matrices(corpusid: str = None,
                       feats: int = 10,
                       words: int = 6,
                       docs_per_feat: int = 0,
                       feats_per_doc: int = 3,
                       path: str = None):
    out = {
        'corpusid': corpusid,
        'feats': feats,
        'error': False
    }
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
        out['error'] = True
        return out

    celery.send_task(RMXBOT_TASKS['nlp_callback'], kwargs={
        'corpusid': corpusid,
        'feats': feats
    })
    return out


@celery.task(bind=True, time_limit=CELERY_TIME_LIMIT)
def compute_matrices(self, **kwds):
    """Computing matrices"""
    features_and_docs(
        path=kwds['path'],
        feats=kwds.get('feats'),
        corpusid=kwds.get('corpusid'),
        words=kwds.get('words'),
        docs_per_feat=kwds.get('docs_per_feat'),
        feats_per_doc=kwds.get('feats_per_doc')
    )
    celery.send_task(RMXBOT_TASKS['nlp_callback'], kwargs={
        'corpusid': kwds.get('corpusid'),
        'feats': kwds.get('feats')
    })
    return kwds


@celery.task(bind=True, time_limit=CELERY_TIME_LIMIT)
def integrity_check(self, corpusid: str = None, path: str = None,
                    tmp_path: str = None):

    check = IntegrityCheck(corpusid=corpusid, path=path)
    check()
    return {
        'corpusid': corpusid,
        'path': path,
        'tmp_path': tmp_path,
    }


@celery.task
def integrity_check_callback(self, kwds):
    """Task called after the integrity check succeeds. This task sends matrices
    to proximity-bot (the server) and deletes the temporary directory.
    :param self:
    :param kwds: dict containing the parameters
    :return:
    """
    corpusid = kwds.get('corpusid')
    path = kwds.get('path')
    tmp_path = kwds.get('tmp_path')
    resp = requests.post(
        INTEGRITY_CHECK_CALLBACK,
        files={
            'file': open(
                shutil.make_archive(
                    os.path.join(tmp_path, 'matrix'),
                    'zip',
                    path,
                    'matrix'
                ),
                'rb')
        },
        data={
            'payload': json.dumps({
                'corpusid': corpusid
            })
        }
    )
    if resp.ok and resp.json().get('success'):
        shutil.rmtree(tmp_path)
