# Standard libraries
import os
import time
from typing import (
    List,
    NamedTuple,
    Tuple,
)

# Third-party libraries
import git
from git.cmd import Git
from pandas import (
    DataFrame,
    Series,
)

# Local libraries
from utils.logs import (
    log,
    log_exception,
)
from utils.repositories import (
    get_commit_hunks,
    get_commit_stats,
    parse_git_shortstat,
)


COMMIT_FEATURES: List[str] = [
    'hunks',
    'additions',
    'deletions',
    'deltas',
    'touched'
]


class CommitFeatures(NamedTuple):
    hunks: int
    additions: int
    deletions: int
    deltas: int
    touched: int


def get_commit_changed_lines(git_repo: Git, commit: str) -> Tuple[int, int]:
    """Get the amount of lines added and deleted in the commit"""
    commit_stats: str = get_commit_stats(git_repo, commit)
    insertions, deletions = parse_git_shortstat(commit_stats)
    return insertions, deletions


def get_features(row: Series, fusion_path: str) -> CommitFeatures:
    additions: int = 0
    deletions: int = 0
    hunks: int = 0
    try:
        repo: str = row['repo']
        commit: str = row['commit']
        repo_path: str = os.path.join(fusion_path, repo)
        git_repo: Git = git.Git(repo_path)
        hunks = get_commit_hunks(repo_path, commit)
        additions, deletions = get_commit_changed_lines(git_repo, commit)
    except KeyError as exc:
        log_exception('info', exc, row=row)
    return CommitFeatures(
        hunks=hunks,
        additions=additions,
        deletions=deletions,
        deltas=additions - deletions,
        touched=additions + deletions
    )


def extract_features(training_df: DataFrame, fusion_path: str) -> bool:
    """Extract features from the commit Git stats and add them to the DF"""
    success: bool = True
    try:
        timer: float = time.time()
        training_df[COMMIT_FEATURES] = training_df.apply(
            get_features,
            args=(fusion_path,),
            axis=1,
            result_type='expand'
        )
        log(
            'info',
            'Features extracted after %.2f seconds',
            time.time() - timer
        )
    except KeyError:
        success = False
    return success
