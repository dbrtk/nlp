import os
import shlex
import subprocess

from .config import (DATA_ROOT, PROXIMITY_BOT_HOSTNAME, PROXIMITY_USER,
                     RSYNC_GET_DATA, RSYNC_GET_VECTORS, RSYNC_POST_DATA)


def sync_corpus_data(
        remote_path: str = None,
        unique_id: str = None,
        get=True,
        get_vectors=False,
        **kwds):

    local_path = os.path.join(DATA_ROOT, unique_id)
    
    if get_vectors:
        command = RSYNC_GET_VECTORS
    elif get:
        command = RSYNC_GET_DATA
    else:
        command = RSYNC_POST_DATA
    
    res = subprocess.run(
        shlex.split("%(command)s %(host)s %(user)s %(remote)s %(local)s" % {
            'command': command,
            'host': PROXIMITY_BOT_HOSTNAME,
            'user': PROXIMITY_USER,
            'remote': remote_path,
            'local': local_path
        }),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if res.returncode == 0:
        return local_path
    raise RuntimeError(local_path)
