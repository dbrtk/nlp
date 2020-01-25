
from .app import celery
from .config.celeryconf import RMXNMF_TASKS


def extract_features(
        containerid: str = None,
        matrix_path: str = None,
        target_path: str = None,
        path: str = None,
        feature_number: int = 10):
    """
    Emitting a task for extracting features.

    :param containerid:
    :param matrix_path:
    :param target_path:
    :param path:
    :param feature_number:
    :return:
    """
    from .task import feat_integrity_check

    celery.send_task(RMXNMF_TASKS['factorize_matrix'], kwargs={
        'matrix_path': matrix_path,
        'target_path': target_path,
        'feature_number': feature_number
    }, link=feat_integrity_check.s(path, containerid, feature_number))


def word_count():

    pass
