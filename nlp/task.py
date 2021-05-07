
from .app import celery
from .config.appconf import CELERY_TIME_LIMIT
from .config.celeryconf import RMXWEB_TASKS
from .data import DataFolder
from .integrity_check import IntegrityCheck
from .views import call_factorize, features_and_docs, kmeans_clust


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
    except (IndexError, Exception,):
        out['error'] = True
        return out

    celery.send_task(RMXWEB_TASKS['nlp_callback'], kwargs={
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
        containerid=kwds.get('corpusid'),
        words=kwds.get('words'),
        docs_per_feat=kwds.get('docs_per_feat'),
        feats_per_doc=kwds.get('feats_per_doc')
    )
    celery.send_task(RMXWEB_TASKS['nlp_callback'], kwargs={
        'corpusid': kwds.get('corpusid'),
        'feats': kwds.get('feats')
    })
    return kwds


@celery.task(bind=True, time_limit=CELERY_TIME_LIMIT)
def integrity_check(self, containerid: str = None, path: str = None):

    check = IntegrityCheck(containerid=containerid, path=path)
    check()

    celery.send_task(RMXWEB_TASKS['integrity_check_callback'], kwargs={
        'containerid': containerid
    })


@celery.task(time_limit=CELERY_TIME_LIMIT)
def available_features(corpusid: str = None, path: str = None):
    """returns available features for a corpusid and a corpus path"""

    return DataFolder(containerid=corpusid, path=path).available_feats


@celery.task(time_limit=CELERY_TIME_LIMIT)
def get_features_and_docs(path: str = None,
                          feats: int = 25,
                          containerid: str = None,
                          words: int = 6,
                          docs_per_feat: int = 3,
                          feats_per_doc: int = 3):
    """ returns features and docs
    it's a celery task that wraps views.features_and_docs
    :param path: path to corpus
    :param feats: number of features
    :param containerid: container id
    :param words: number of words per feature
    :param docs_per_feat: documents per feature
    :param feats_per_doc: features per document
    :return:
    """
    return features_and_docs(path=path,
                             feats=feats,
                             containerid=containerid,
                             words=words,
                             docs_per_feat=docs_per_feat,
                             feats_per_doc=feats_per_doc)


@celery.task
def feat_integrity_check(path: str, containerid: str, feature_number: int):
    """

    :param path:
    :param containerid:
    :param feature_number:
    :return:
    """
    inst = DataFolder(containerid=containerid, path=path, featcount=feature_number)
    inst.check_wf_folder_structure()


@celery.task
def kmeans_cluster(containerid: str = None, path: str = None, k: int = 10):
    """

    :param containerid:
    :param path:
    :param k:
    :return:
    """
    return kmeans_clust(containerid, path, k)


@celery.task
def kmeans_files(containerid: str = None, path: str = None):
    """

    :param containerid:
    :param path:
    :return:
    """
    return DataFolder(containerid=containerid, path=path).kmeans_files()
