# Standard libraries
import os
import random
import time
from typing import (
    Dict,
    List,
    Tuple,
)

# Third-party libraries
import git
import pandas as pd
from git.cmd import Git
from pandas import DataFrame

# Local libraries
from features.commit import extract_features
from utils.logs import log
from utils.repositories import (
    get_bad_repos,
    get_file_commit_history,
    get_repository_commit_history,
)
from utils.training import get_vulnerable_files


COMMIT_MAX_RETRIES: int = 15


def build_training_df(group: str, fusion_path: str) -> DataFrame:
    """Creates a training DataFrame with vulnerable and safe commits"""
    ignore_repos: List[str] = get_bad_repos(fusion_path)
    vuln_files: List[str] = get_vulnerable_files(group, ignore_repos)
    vuln_commits, vuln_repos = get_initial_commits_and_repos(
        vuln_files,
        fusion_path
    )
    safe_commits, safe_repos = get_safe_commits_and_repos(
        vuln_commits,
        fusion_path,
        ignore_repos
    )
    return pd.concat([
        pd.DataFrame({
            'repo': vuln_repos,
            'commit': vuln_commits,
            'is_vuln': 1
        }),
        pd.DataFrame({
            'repo': safe_repos,
            'commit': safe_commits,
            'is_vuln': 0
        })
    ])


def get_initial_commits_and_repos(
    vuln_files: List[str],
    fusion_path: str
) -> Tuple[List[str], List[str]]:
    """Gets the commit that introduced each file"""
    vuln_commits: List[str] = []
    vuln_repos: List[str] = []
    for file in vuln_files:
        repo: str = file.split(os.path.sep)[0]
        file_relative_path: str = os.path.sep.join(file.split(os.path.sep)[1:])
        git_repo: Git = git.Git(os.path.join(fusion_path, repo))
        commit_history: List[str] = get_file_commit_history(
            git_repo,
            file_relative_path
        )
        if commit_history and commit_history[-1] not in vuln_commits:
            vuln_commits.append(commit_history[-1])
            vuln_repos.append(repo)

    return vuln_commits, vuln_repos


def get_safe_commits_and_repos(
    vuln_commits: List[str],
    fusion_path: str,
    ignore_repos: List[str]
) -> Tuple[List[str], List[str]]:
    """Fetches random commits where a vulnerabile file was not introduced"""
    timer: float = time.time()
    safe_commits: List[str] = []
    safe_repos: List[str] = []
    repo_commits: Dict[str, List[str]] = {}
    retries: int = 0
    allowed_repos: List[str] = [
        repo
        for repo in os.listdir(fusion_path)
        if repo not in ignore_repos
    ]
    while len(safe_commits) < len(vuln_commits):
        if retries > COMMIT_MAX_RETRIES:
            log(
                'info',
                'Could not find enough safe commits to balance the vulnerable '
                'ones'
            )
            break
        repo = random.choice(allowed_repos)
        git_repo: Git = git.Git(os.path.join(fusion_path, repo))
        if repo not in repo_commits.keys():
            repo_commits[repo] = get_repository_commit_history(git_repo)
        rand_commit: str = random.choice(repo_commits[repo])
        if rand_commit not in vuln_commits and rand_commit not in safe_commits:
            safe_commits.append(rand_commit)
            safe_repos.append(repo)
            retries = 0
        retries += 1
    log(
        'info',
        'Safe commits extracted after %.2f seconds',
        time.time() - timer
    )
    return safe_commits, safe_repos


def get_subscription_commit_metadata(subscription_path: str) -> bool:
    """Creates CSV with the commit features of the subscription files"""
    success: bool = True
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    if os.path.exists(fusion_path):
        training_df: DataFrame = build_training_df(group, fusion_path)
        if training_df.empty:
            success = False
            log(
                'info',
                'Group %s does not have any vulnerabilities of type "lines"',
                group
            )
        else:
            success = extract_features(training_df, fusion_path)
            if success:
                csv_name: str = f'{group}_commit_features.csv'
                training_df.to_csv(csv_name, index=False)
                log('info', 'Features extracted succesfully to %s', csv_name)
    else:
        success = False
        log('info', 'Fusion folder for group %s does not exist', group)
    return success
