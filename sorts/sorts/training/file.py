# Standard libraries
import os
import random
import time
from typing import (
    Dict,
    List,
    Set,
    Tuple,
)

# Third-party libraries
import pandas as pd
from pandas import DataFrame

# Local libraries
from integrates.domain import get_vulnerable_lines
from utils.logs import (
    blocking_log,
    log,
)
from utils.repositories import get_bad_repos
from utils.static import read_allowed_names


# Consstants
MAX_RETRIES: int = 15


async def build_vulnerabilities_df(group: str, fusion_path: str) -> DataFrame:
    """
    Creates a DataFrame with a balanced number of vulnerable and safe files
    extracted from the Integrates API and the subscription repositories
    """
    timer: float = time.time()
    await log('info', 'Building vulnerabilities DataFrame...')
    vuln_files, vuln_repos = await get_unique_vuln_files(group)
    vuln_files, vuln_repos = await filter_vuln_files(
        vuln_files, vuln_repos, fusion_path
    )
    await log(
        'info',
        'Vulnerable files extracted after %.2f seconds',
        time.time() - timer
    )

    timer = time.time()
    safe_files = get_safe_files(vuln_files, vuln_repos, fusion_path)
    await log(
        'info',
        'Safe files extracted after %.2f seconds',
        time.time() - timer
    )

    vulns_df = pd.concat([
        pd.DataFrame(
            map(lambda x: (x, 1), vuln_files),
            columns=['file', 'is_vuln']
        ),
        pd.DataFrame(
            map(lambda x: (x, 0), safe_files),
            columns=['file', 'is_vuln']
        ),
    ])
    vulns_df['repo'] = vulns_df['file'].apply(
        lambda filename: os.path.join(
            fusion_path, filename.split(os.path.sep)[0]
        )
    )
    vulns_df.reset_index(drop=True, inplace=True)
    return vulns_df


async def filter_vuln_files(
    vuln_files: List[str],
    vuln_repos: List[str],
    fusion_path: str
) -> Tuple[List[str], List[str]]:
    """
    Filter files that comply with certain extensions and remove
    binaries and files that beloong in bad repositories
    """
    filtered_vuln_files: List[str] = []
    extensions, composites = read_allowed_names()
    bad_repos = await get_bad_repos(fusion_path, vuln_repos)
    for vuln_file in vuln_files:
        vuln_repo: str = vuln_file.split(os.path.sep)[0]
        vuln_file_name: str = os.path.basename(vuln_file)
        if vuln_repo not in bad_repos:
            vuln_file_extension: str = os.path.splitext(vuln_file_name)[1]\
                .strip('.')
            if vuln_file_extension in extensions or \
                    vuln_file_name in composites:
                filtered_vuln_files.append(vuln_file)
    return (
        filtered_vuln_files,
        [repo for repo in vuln_repos if repo not in bad_repos]
    )


async def get_project_data(subscription_path: str) -> bool:
    """
    Creates a CSV file with all the features extracted for each file of every
    repository of the defined subscription
    """
    success: bool = True
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    vulns_df = await build_vulnerabilities_df(group, fusion_path)
    if vulns_df.empty:
        success = False
        await log(
            'info',
            'Group %s does not have any vulnerabilities of type "lines"',
            group
        )
    else:
        csv_name: str = f'{group}_files_features.csv'
        vulns_df.to_csv(csv_name, index=False)
        await log('info', 'Features extracted succesfully to %s', csv_name)
    return success


def get_safe_files(
    vuln_files: List[str],
    vuln_repos: List[str],
    fusion_path: str
) -> List[str]:
    safe_files: Set[str] = set()
    repo_files: Dict[str, List[str]] = {}
    retries: int = 0

    extensions, composites = read_allowed_names()
    while len(safe_files) < len(vuln_files):
        if retries > MAX_RETRIES:
            blocking_log(
                'info',
                'Could not find enough safe files to balance the DataFrame'
            )
            break
        repo = random.choice(vuln_repos)
        if repo not in repo_files.keys():
            repo_files[repo] = [
                os.path.join(path, filename).replace(
                    f'{fusion_path}{os.path.sep}', ''
                )
                for path, _, files in os.walk(os.path.join(fusion_path, repo))
                for filename in files
            ]
        file = random.choice(repo_files[repo]) if repo_files[repo] else ''
        if (
            file and
            file not in vuln_files and
            file not in composites and
            os.path.splitext(file)[1].strip('.') in extensions
        ):
            safe_files.add(file)
            retries = 0
        retries += 1
    return sorted(safe_files)


async def get_unique_vuln_files(group: str) -> Tuple[List[str], List[str]]:
    """
    Filter unique values of vulnerable files and their respective repositories
    """
    vulnerabilities = await get_vulnerable_lines(group)
    unique_vuln_files: Set[str] = {vuln.where for vuln in vulnerabilities}
    unique_vuln_repos: Set[str] = {
        where.split('/')[0] for where in unique_vuln_files
    }
    return sorted(unique_vuln_files), sorted(unique_vuln_repos)
