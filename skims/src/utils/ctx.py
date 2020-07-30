# Standard library
from os.path import (
    abspath,
    dirname,
    join,
)

# Constants
ROOT: str = abspath(dirname(dirname(dirname(__file__))))


def get_artifact(path: str) -> str:
    return abspath(join(ROOT, path))
