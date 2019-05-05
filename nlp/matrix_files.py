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

    # todo(): get rid of chmod!
    # def chmod(path):
    #     os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    # chmod(path)
    # for root, dirs, files in os.walk(path):
    #     for f in files:
    #         chmod(os.path.join(root, f))
    #     for d in dirs:
    #         chmod(os.path.join(root, d))
    return path


def unpack_vectors(tmp_upload_path: str = None, unique_id: str = None):

    path = os.path.join(DATA_ROOT, unique_id)
    shutil.unpack_archive(tmp_upload_path, path, 'zip')
    return path
