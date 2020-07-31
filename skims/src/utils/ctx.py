# Standard library
from os.path import (
    abspath,
    dirname,
    exists,
    join,
)

# Constants
ROOT: str = abspath(dirname(dirname(dirname(__file__))))


def get_artifact(path: str) -> str:
    for attempt in [
        abspath(join(ROOT, path)),
        abspath(join(ROOT, 'site-packages', path)),
    ]:
        if exists(attempt):
            return attempt

    raise FileNotFoundError(path)
