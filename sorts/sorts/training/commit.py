# Standard libraries
import os
from typing import List

# Third-party libraries
import git
import pandas as pd
from git.cmd import Git
from pandas import DataFrame

# Local libraries
from utils.logs import log
from utils.repositories import (
    get_bad_repos,
    get_file_commit_history,
)
from utils.training import get_vulnerable_files


COMMIT_MAX_RETRIES: int = 15


def build_training_df(group: str, fusion_path: str) -> DataFrame:
    """Creates a training DataFrame with vulnerable and safe commits"""
    ignore_repos: List[str] = get_bad_repos(fusion_path)
    vuln_files: List[str] = get_vulnerable_files(group, ignore_repos)
    vuln_commits: List[str] = get_initial_commit(vuln_files, fusion_path)
    return pd.DataFrame({'file': vuln_files, 'commit': vuln_commits})


def get_initial_commit(vuln_files: List[str], fusion_path: str) -> List[str]:
    """Gets the commit that introduced each file"""
    vuln_commits: List[str] = []
    for file in vuln_files:
        repo: str = file.split(os.path.sep)[0]
        file_relative_path: str = os.path.sep.join(file.split(os.path.sep)[1:])
        initial_commit: str = '-'
        git_repo: Git = git.Git(os.path.join(fusion_path, repo))
        commit_history: List[str] = get_file_commit_history(
            git_repo,
            file_relative_path
        )
        if commit_history:
            initial_commit = commit_history[-1]
        vuln_commits.append(initial_commit)
    return vuln_commits


def get_subscription_commit_metadata(subscription_path: str) -> bool:
    """Creates CSV with the commit features of the subscription files"""
    success: bool = True
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    training_df: DataFrame = build_training_df(group, fusion_path)
    if training_df.empty:
        success = False
        log(
            'info',
            'Group %s does not have any vulnerabilities of type "lines"',
            group
        )
    else:
        csv_name: str = f'{group}_commit_features.csv'
        training_df.to_csv(csv_name, index=False)
        log('info', 'Features extracted succesfully to %s', csv_name)
    return success
