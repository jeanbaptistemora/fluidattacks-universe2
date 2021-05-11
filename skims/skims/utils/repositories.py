# Standard libraries
import contextlib
from typing import (
    Optional,
)

# Third party libraries
from git import (
    Repo,
    GitCommandError,
    InvalidGitRepositoryError,
    NoSuchPathError,
)
from unidiff import (
    PatchSet,
)

# Constants
DEFAULT_COMMIT: str = "0000000000000000000000000000000000000000"


def get_repo(path: str) -> Repo:
    return Repo(path, search_parent_directories=True)


def get_repo_head_hash(path: str) -> str:
    with contextlib.suppress(InvalidGitRepositoryError, NoSuchPathError):
        repo: Repo = get_repo(path)
        head_hash: str = repo.head.commit.hexsha
        return head_hash

    return DEFAULT_COMMIT


def get_diff(
    repo: Repo,
    *,
    rev_a: str,
    rev_b: str = "HEAD",
) -> Optional[PatchSet]:
    with contextlib.suppress(GitCommandError):
        patch = PatchSet(
            repo.git.diff(
                "--color=never",
                "--minimal",
                "--patch",
                "--unified=0",
                f"{rev_a}...{rev_b}",
            ),
        )

        return patch

    return None
