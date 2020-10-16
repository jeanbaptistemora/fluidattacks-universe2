# Standard libraries
import os
import time
from datetime import datetime
from typing import (
    List,
    NamedTuple,
    Tuple,
    Set,
)

# Third-party libraries
import git
from git.cmd import Git
from git.exc import GitCommandError
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
    get_commit_date,
    get_commit_files,
    get_commit_hunks,
    get_commit_stats,
    get_file_authors_history,
    parse_git_shortstat,
)


COMMIT_FEATURES: List[str] = [
    'hunks',
    'additions',
    'deletions',
    'deltas',
    'touched',
    'touched_files',
    'max_others_touchers',
    'touches_busy_file',
    'authored_hour'
]


class CommitFeatures(NamedTuple):
    hunks: int
    additions: int
    deletions: int
    deltas: int
    touched: int
    touched_files: int
    max_other_touchers: int
    touches_busy_file: int
    authored_hour: int


def get_commit_changed_lines(git_repo: Git, commit: str) -> Tuple[int, int]:
    """Get the amount of lines added and deleted in the commit"""
    commit_stats: str = get_commit_stats(git_repo, commit)
    insertions, deletions = parse_git_shortstat(commit_stats)
    return insertions, deletions


def get_commit_files_authors(git_repo: Git, commit: str) -> List[int]:
    """Gets the number of authors that have modified the commit files"""
    files_authors: List[int] = []
    files: List[str] = get_commit_files(git_repo, commit)
    for file in files:
        try:
            authors: Set[str] = set(get_file_authors_history(git_repo, file))
            files_authors.append(len(authors))
        except GitCommandError:
            # This is triggered when a file that was modified in the commit
            # does not exist in the current version of the repository
            pass
    return files_authors


def get_commit_hour(git_repo: Git, commit: str) -> int:
    """Gets the hour when a change was commmited"""
    commit_date: datetime = get_commit_date(git_repo, commit)
    return commit_date.hour


def get_features(row: Series, fusion_path: str) -> CommitFeatures:
    additions: int = 0
    authored_hour: int = 0
    files_authors: List[int] = []
    deletions: int = 0
    hunks: int = 0
    max_other_touchers: int = 0
    try:
        repo: str = row['repo']
        commit: str = row['commit']
        repo_path: str = os.path.join(fusion_path, repo)
        git_repo: Git = git.Git(repo_path)
        hunks = get_commit_hunks(repo_path, commit)
        additions, deletions = get_commit_changed_lines(git_repo, commit)
        files_authors = get_commit_files_authors(git_repo, commit)
        max_other_touchers = max(files_authors) if files_authors else 0
        authored_hour = get_commit_hour(git_repo, commit)
    except KeyError as exc:
        log_exception('info', exc, row=row)
    return CommitFeatures(
        hunks=hunks,
        additions=additions,
        deletions=deletions,
        deltas=additions - deletions,
        touched=additions + deletions,
        touched_files=len(files_authors),
        max_other_touchers=max_other_touchers,
        touches_busy_file=1 if max_other_touchers > 9 else 0,
        authored_hour=authored_hour
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
