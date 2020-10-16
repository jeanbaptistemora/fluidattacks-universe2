# Standard libraries
import time
import os
from datetime import datetime
from functools import partial
from typing import (
    List,
    NamedTuple,
    Set,
)

# Third-party libraries
import git
import pytz
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
    get_file_authors_history,
    get_file_commit_history,
    get_file_date_history,
    get_file_stat_history,
    parse_git_shortstat,
)


FILE_FEATURES = [
    'num_commits',
    'num_unique_authors',
    'file_age',
    'midnight_commits',
    'risky_commits',
    'seldom_contributors'
    'busy_file',
    'commit_frequency',
    'num_lines',
]
FILE_FEATURES = [
    'num_commits',
    'num_unique_authors',
    'file_age',
    'midnight_commits',
    'risky_commits',
    'seldom_contributors',
    'num_lines',
    'commit_frequency',
    'busy_file'
]


class FileFeatures(NamedTuple):
    num_commits: int
    num_unique_authors: int
    file_age: int
    midnight_commits: int
    risky_commits: int
    seldom_contributors: int
    num_lines: int
    commit_frequency: float
    busy_file: int


def get_features(row: Series) -> FileFeatures:
    # Use -1 as default value to avoid ZeroDivisionError
    file_age: int = -1
    midnight_commits: int = -1
    num_commits: int = -1
    num_lines: int = -1
    risky_commits: int = -1
    seldom_contributors: int = -1
    unique_authors: Set[str] = set()
    try:
        repo_path: str = row['repo']
        repo_name: str = os.path.basename(repo_path)
        git_repo: Git = git.Git(repo_path)
        file_relative: str = row['file'].replace(f'{repo_name}/', '', 1)
        file_age = get_file_age(git_repo, file_relative)
        midnight_commits = get_midnight_commits(git_repo, file_relative)
        num_commits = get_num_commits(git_repo, file_relative)
        num_lines = get_num_lines(
            os.path.join(git_repo.working_dir, file_relative)
        )
        risky_commits = get_risky_commits(git_repo, file_relative)
        seldom_contributors = get_seldom_contributors(git_repo, file_relative)
        unique_authors = get_unique_authors(git_repo, file_relative)
    except (
        KeyError,
        ValueError
    ) as exc:
        log_exception('info', exc, row=row)
    return FileFeatures(
        num_commits=num_commits,
        num_unique_authors=len(unique_authors),
        file_age=file_age,
        midnight_commits=midnight_commits,
        risky_commits=risky_commits,
        seldom_contributors=seldom_contributors,
        num_lines=num_lines,
        commit_frequency=round(num_commits / file_age, 4),
        busy_file=1 if len(unique_authors) > 9 else 0
    )


def get_file_age(git_repo: Git, file: str) -> int:
    """Gets the number of days since the file was created"""
    today: datetime = datetime.now(pytz.utc)
    commit_date_history: List[str] = get_file_date_history(git_repo, file)
    file_creation_date: str = commit_date_history[-1]
    return (today - datetime.fromisoformat(file_creation_date)).days


def get_num_commits(git_repo: Git, file: str) -> int:
    """Gets the number of commits that have modified a file"""
    commit_history: List[str] = get_file_commit_history(git_repo, file)
    return len(commit_history)


def get_num_lines(file_path: str) -> int:
    """Gets the numberr of lines that a file has"""
    result: int = 0
    try:
        file = open(file_path, 'rb')
        bufgen = iter(
            partial(file.raw.read, 1024 * 1024), b''  # type: ignore
        )
        result = sum(buf.count(b'\n') for buf in bufgen)
    except FileNotFoundError:
        print(f'File {file_path} not found. ')
    return result


def get_midnight_commits(git_repo: Git, file: str) -> int:
    """Gets the number of times a file was modified between 0 AM -6 AM"""
    commit_date_history: List[str] = get_file_date_history(git_repo, file)
    commit_hour_history: List[int] = [
        datetime.fromisoformat(date).hour for date in commit_date_history
    ]
    return sum([1 for hour in commit_hour_history if 0 <= hour < 6])


def get_risky_commits(git_repo: Git, file: str) -> int:
    """Gets the number of commits which had more than 200 deltas"""
    risky_commits: int = 0
    commit_stat_history: List[str] = get_file_stat_history(git_repo, file)
    for stat in commit_stat_history:
        insertions, deletions = parse_git_shortstat(stat)
        if insertions + deletions > 200:
            risky_commits += 1
    return risky_commits


def get_seldom_contributors(git_repo: Git, file: str) -> int:
    """Gets the number of authors that contributed below the average"""
    seldom_contributors: int = 0
    authors_history: List[str] = get_file_authors_history(git_repo, file)
    unique_authors: Set[str] = set(authors_history)
    avg_commit_per_author: float = round(
        len(authors_history) / len(unique_authors),
        4
    )
    for author in unique_authors:
        commits: int = authors_history.count(author)
        if commits < avg_commit_per_author:
            seldom_contributors += 1
    return seldom_contributors


# TODO: use mailmaps to filter possible noise due to bad git management
def get_unique_authors(git_repo: Git, file: str) -> Set[str]:
    """Gets the number of unique authors that modified a file"""
    authors_history: List[str] = get_file_authors_history(git_repo, file)
    return set(authors_history)


def extract_features(training_df: DataFrame) -> bool:
    """Extract features from the file Git history and add them to the DF"""
    success: bool = True
    try:
        timer: float = time.time()
        training_df[FILE_FEATURES] = training_df.apply(
            get_features,
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
