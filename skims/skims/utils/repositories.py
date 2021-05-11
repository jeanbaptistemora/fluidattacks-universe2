# Standard libraries
import contextlib
from typing import (
    NamedTuple,
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
    Hunk,
    PatchedFile,
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
    rev_b: str,
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


class RebaseResult(NamedTuple):
    path: str
    line: int


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    hunk: Hunk
    patch: PatchedFile

    if diff := get_diff(repo, rev_a=rev_a, rev_b=rev_b):
        for patch in diff:

            if patch.source_file == f"a/{path}":
                # The original file matches the path to rebase
                # Let's process the hunks to see what should be done with
                # the line
                for hunk in patch:
                    hunk_source_end = (
                        hunk.source_start + hunk.source_length - 1
                    )

                    if line < hunk.source_start:
                        # The line exists before the hunk and therefore
                        # we do not need to modify the line
                        pass
                    elif line > hunk_source_end:
                        # The line exists after this hunk and therefore
                        # we should increase/decrease the line number
                        line -= hunk_source_end - hunk.source_start
                    elif hunk.source_start <= line <= hunk_source_end:
                        # We cannot rebase because the line was modified
                        # by this hunk
                        # We cannot guess the next position of the line
                        # deterministically
                        return None

                    print(repr(hunk))
        return RebaseResult(path=path, line=line)

    return None
