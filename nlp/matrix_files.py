""" Copying matrix files from the file server (the one that runs rmxbot) to the
    nlp server. This module uses rmxbin (https://github.com/dbrtk/rmxbin) to
    do this.
"""

import os
import shutil

from .config.appconf import DATA_ROOT


def unpack_corpus(tmp_upload_path: str = None, unique_id: str = None):

    path = os.path.join(DATA_ROOT, unique_id)
    shutil.unpack_archive(tmp_upload_path, path, 'zip')
    if os.path.exists(tmp_upload_path):
        os.remove(tmp_upload_path)

    return path


def unpack_vectors(tmp_upload_path: str = None, unique_id: str = None):

    path = os.path.join(DATA_ROOT, unique_id)
    shutil.unpack_archive(tmp_upload_path, path, 'zip')
    if os.path.exists(tmp_upload_path):
        os.remove(tmp_upload_path)
    return path
