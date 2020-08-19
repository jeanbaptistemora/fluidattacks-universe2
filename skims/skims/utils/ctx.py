# Standard library
from multiprocessing import (
    Manager,
)
from multiprocessing.managers import (
    SyncManager,
)
from os.path import (
    abspath,
    dirname,
    exists,
    join,
)
from typing import (
    Any,
)

# Constants
MANAGER: SyncManager = Manager()
NAMESPACE: Any = MANAGER.Namespace()
ROOT: str = abspath(dirname(dirname(dirname(__file__))))


def get_artifact(path: str) -> str:
    for attempt in [
        abspath(join(ROOT, path)),
        abspath(join(ROOT, 'site-packages', path)),
    ]:
        if exists(attempt):
            return attempt

    raise FileNotFoundError(path)


def read_artifact(path: str) -> bytes:
    with open(get_artifact(path), mode='rb') as file:
        return file.read()
