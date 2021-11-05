from git import (
    GitError,
    Repo,
)
from more_itertools import (
    pairwise,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)
from unidiff import (
    Hunk,
    PatchedFile,
    PatchSet,
)
from utils.logs import (
    log_blocking,
)

# Constants
DEFAULT_COMMIT: str = "0000000000000000000000000000000000000000"


def get_repo(path: str, search_parent_directories: bool = True) -> Repo:
    return Repo(path, search_parent_directories=search_parent_directories)


def get_repo_head_hash(path: str) -> str:
    try:
        repo: Repo = get_repo(path)
        head_hash: str = repo.head.commit.hexsha
        return head_hash
    except GitError as exc:
        log_blocking("error", "Computing commit hash: %s ", exc)

    return DEFAULT_COMMIT


def get_diff(
    repo: Repo,
    *,
    rev_a: str,
    rev_b: str,
) -> PatchSet:
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


class RebaseResult(NamedTuple):
    path: str
    line: int
    rev: str


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    rev: str = rev_a
    revs_str: str = repo.git.log(
        "--format=%H",
        "--reverse",
        f"{rev_a}...{rev_b}",
    )
    revs: List[str] = [rev_a] + revs_str.splitlines()

    # Let's rebase one commit at a time,
    # this way we reduce the probability of conflicts
    # and ensure line numbers are updated up to the latest possible commit
    for rev_1, rev_2 in pairwise(revs):
        if rebase_result := _rebase_one_commit_at_a_time(
            repo, path=path, line=line, rev_a=rev_1, rev_b=rev_2
        ):
            path = rebase_result.path
            line = rebase_result.line
            rev = rebase_result.rev
        else:
            # We cannot continue rebasing
            break

    if rev == rev_a:
        # We did not rebase anything
        return None

    return RebaseResult(path=path, line=line, rev=rev)


def _rebase_one_commit_at_a_time(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    hunk: Hunk
    patch: PatchedFile

    diff = get_diff(repo, rev_a=rev_a, rev_b=rev_b)
    for patch in diff:
        if patch.source_file == f"a/{path}":
            if patch.is_removed_file:
                # We cannot rebase something that was deleted
                return None
            # The original file matches the path to rebase
            # If the file was moved or something, this updates the path
            path = patch.target_file[2:]

            # Let's process the hunks to see what should be done with
            # the line numbers
            for hunk in patch:
                hunk_source_end = hunk.source_start + hunk.source_length - 1

                if line < hunk.source_start:
                    # The line exists before the hunk and therefore
                    # we do not need to modify the line
                    pass
                elif line > hunk_source_end:
                    # The line exists after this hunk and therefore
                    # we should increase/decrease the line number
                    line += hunk.added - hunk.removed
                elif hunk.source_start <= line <= hunk_source_end:
                    # We cannot rebase because the line was modified
                    # by this hunk
                    # We cannot guess the next position of the line
                    # deterministically
                    return None

    return RebaseResult(path=path, line=line, rev=rev_b)
