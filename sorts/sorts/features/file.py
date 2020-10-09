# Standard libraries
import time
import os
from typing import List

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
from utils.repositories import get_file_commit_history


def get_num_commits(row: Series) -> int:
    """Get the number of commits that have modified a file"""
    commit_history: List[str] = []
    try:
        repo_path: str = row['repo']
        repo_name: str = os.path.basename(repo_path)
        git_repo: Git = git.Git(repo_path)
        file_relative: str = row['file'].replace(f'{repo_name}/', '', 1)
        commit_history = get_file_commit_history(git_repo, file_relative)
    except KeyError as exc:
        log_exception('error', exc, feature='num_commits', row=row)
    return len(commit_history)


def extract_features(training_df: DataFrame) -> None:
    """Extract features from the file Git history and add them to the DF"""
    timer: float = time.time()
    training_df['num_commits'] = training_df.apply(get_num_commits, axis=1)
    log('info', 'Features extracted after %.2f seconds', time.time() - timer)
