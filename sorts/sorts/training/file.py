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
from utils.logs import log
from utils.repositories import (
    get_bad_repos,
    get_repository_files,
)
from utils.static import read_allowed_names
from utils.training import get_vulnerable_files


# Constants
FILE_MAX_RETRIES: int = 15


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


def get_subscription_file_metadata(subscription_path: str) -> bool:
    """Creates a CSV with the file features from the subscription"""
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
            success = extract_features(training_df)
            if success:
                csv_name: str = f'{group}_files_features.csv'
                training_df.to_csv(csv_name, index=False)
                log('info', 'Features extracted succesfully to %s', csv_name)
    else:
        success = False
        log('info', 'Fusion folder for group %s does not exist', group)
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
    if allowed_repos:
        while len(safe_files) < len(vuln_files):
            if retries > FILE_MAX_RETRIES:
                log(
                    'info',
                    'Could not find enough safe files to balance the '
                    'vulnerable ones'
                )
                break

            repo: str = random.choice(allowed_repos)
            if repo not in repo_files.keys():
                repo_files[repo] = get_repository_files(
                    os.path.join(fusion_path, repo)
                )
            if repo_files[repo]:
                file: str = random.choice(repo_files[repo])
                file_extension: str = os.path.splitext(file)[1].strip('.')
                if (
                    file not in vuln_files and
                    file not in safe_files and
                    (file in composites or file_extension in extensions)
                ):
                    safe_files.add(file)
                    retries = 0
            retries += 1
        log(
            'info',
            'Safe files extracted after %.2f secods',
            time.time() - timer
        )
    return sorted(safe_files)
