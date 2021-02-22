# Standard libraries
import contextlib
import os

# Third party libraries
from git import (
    Repo,
    InvalidGitRepositoryError,
    NoSuchPathError,
)

# Constants
DEFAULT_COMMIT: str = '0000000000000000000000000000000000000000'


def get_repository(path: str) -> Repo:
    return Repo(path, search_parent_directories=True)


def get_repository_head_hash(path: str) -> str:
    path = os.path.abspath(path)
    if os.path.isfile(path):
        path = os.path.dirname(path)

    with contextlib.suppress(InvalidGitRepositoryError, NoSuchPathError):
        repo: Repo = get_repository(path)
        head_hash: str = repo.head.commit.hexsha
        return head_hash

    return DEFAULT_COMMIT
