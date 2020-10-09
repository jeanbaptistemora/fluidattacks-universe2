# Standard libraries
import os
import random
import time
from typing import (
    Dict,
    List,
    Set,
)

# Third-party libraries
import pandas as pd
from pandas import DataFrame

# Local libraries
from features.file import extract_features
from integrates.domain import get_vulnerable_lines
from utils.logs import log
from utils.repositories import (
    get_bad_repos,
    get_repository_files,
)
from utils.static import read_allowed_names


# Consstants
MAX_RETRIES: int = 15


def build_training_df(group: str, fusion_path: str) -> DataFrame:
    """Creates a training DataFrame with vulnerable and safe files"""
    ignore_repos: List[str] = get_bad_repos(fusion_path)
    vuln_files: List[str] = get_vulnerable_files(group, ignore_repos)
    safe_files = get_safe_files(vuln_files, ignore_repos, fusion_path)

    training_df = pd.concat([
        pd.DataFrame(
            map(lambda x: (x, 1), vuln_files),
            columns=['file', 'is_vuln']
        ),
        pd.DataFrame(
            map(lambda x: (x, 0), safe_files),
            columns=['file', 'is_vuln']
        ),
    ])
    training_df['repo'] = training_df['file'].apply(
        lambda filename: os.path.join(
            fusion_path, filename.split(os.path.sep)[0]
        )
    )
    training_df.reset_index(drop=True, inplace=True)
    return training_df


def get_vulnerable_files(
    group: str,
    ignore_repos: List[str]
) -> List[str]:
    """Gets vulnerable files to fill the training DataFrame"""
    timer: float = time.time()
    unique_vuln_files: List[str] = get_unique_vuln_files(group)
    allowed_vuln_files: List[str] = filter_allowed_files(
        unique_vuln_files, ignore_repos
    )
    log(
        'info',
        'Vulnerable files extracted after %.2f seconds',
        time.time() - timer
    )
    return allowed_vuln_files


def filter_allowed_files(
    vuln_files: List[str],
    ignore_repos: List[str]
) -> List[str]:
    """Leave files with allowed names and filter out from ignored repos"""
    allowed_vuln_files: List[str] = []
    extensions, composites = read_allowed_names()
    for vuln_file in vuln_files:
        vuln_repo: str = vuln_file.split(os.path.sep)[0]
        if vuln_repo not in ignore_repos:
            vuln_file_name: str = os.path.basename(vuln_file)
            vuln_file_extension: str = os.path.splitext(vuln_file_name)[1]\
                .strip('.')
            if (
                vuln_file_extension in extensions or
                vuln_file_name in composites
            ):
                allowed_vuln_files.append(vuln_file)
    return allowed_vuln_files


def get_subscription_data(subscription_path: str) -> bool:
    """Creates a CSV with the file features from the subscription"""
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
        extract_features(training_df)
        csv_name: str = f'{group}_files_features.csv'
        training_df.to_csv(csv_name, index=False)
        log('info', 'Features extracted succesfully to %s', csv_name)
    return success


def get_safe_files(
    vuln_files: List[str],
    ignore_repos: List[str],
    fusion_path: str
) -> List[str]:
    """Fetches random files that do not have any vulnerability reported"""
    timer: float = time.time()
    safe_files: Set[str] = set()
    repo_files: Dict[str, List[str]] = {}
    retries: int = 0

    extensions, composites = read_allowed_names()
    allowed_repos: List[str] = [
        repo
        for repo in os.listdir(fusion_path)
        if repo not in ignore_repos
    ]
    while len(safe_files) < len(vuln_files):
        if retries > MAX_RETRIES:
            log(
                'info',
                'Could not find enough safe files to balance the DataFrame'
            )
            break

        repo: str = random.choice(allowed_repos)
        if repo not in repo_files.keys():
            repo_files[repo] = get_repository_files(
                os.path.join(fusion_path, repo)
            )
        file: str = random.choice(repo_files.get(repo, ['']))
        if file:
            file_extension: str = os.path.splitext(file)[1].strip('.')
            if (
                file not in vuln_files and
                (file in composites or file_extension in extensions)
            ):
                safe_files.add(file)
            retries = 0
        retries += 1
    log('info', 'Safe files extracted after %.2f secods', time.time() - timer)
    return sorted(safe_files)


def get_unique_vuln_files(group: str) -> List[str]:
    """Removes repeated files from group vulnerabilities"""
    unique_vuln_files: Set[str] = set(get_vulnerable_lines(group))
    return sorted(unique_vuln_files)
