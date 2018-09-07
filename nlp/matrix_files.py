import os
import shlex
import subprocess

from .config import (DATA_ROOT, PROXIMITY_BOT_HOST, PROXIMITY_USER,
                     RSYNC_GET_DATA, RSYNC_POST_DATA)


def sync_corpus_data(
        corpusid: str = None,
        remote_path: str = None,
        unique_id: str = None,
        get=True):

    local_path = os.path.join(DATA_ROOT, unique_id)
    res = subprocess.run(
        shlex.split("%(command)s %(host)s %(user)s %(remote)s %(local)s" % {
            'command': RSYNC_GET_DATA if get else RSYNC_POST_DATA,
            'host': PROXIMITY_BOT_HOST,
            'user': PROXIMITY_USER,
            'remote': remote_path,
            'local': local_path
        }),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if res.returncode == 0 and os.path.isdir(local_path):
        return local_path
    else:
        raise RuntimeError(local_path)
