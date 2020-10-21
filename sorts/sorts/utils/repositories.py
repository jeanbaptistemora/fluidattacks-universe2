# Standard libraries
import os
import re
from datetime import datetime
from typing import (
    Dict,
    List,
    Tuple,
    TypedDict,
)

# Third-party libraries
import git
from git.cmd import Git
from git.exc import (
    GitCommandError,
    GitCommandNotFound,
)
from numpy import ndarray
from pydriller.metrics.process.hunks_count import HunksCount

# Local libraries
from utils.logs import log_exception


STAT_REGEX = re.compile(
    r'([0-9]+ files? changed)?'
    r'(, (?P<insertions>[0-9]+) insertions\(\+\))?'
    r'(, (?P<deletions>[0-9]+) deletions\(\-\))?'
)
RENAME_REGEX = re.compile(
    r'(?P<pre_path>.*)?'
    r'{(?P<old_name>.*) => (?P<new_name>.*)}'
    r'(?P<post_path>.*)?'
)


class GitMetrics(TypedDict):
    author_email: List[str]
    commit_hash: List[str]
    date_iso_format: List[str]
    stats: List[str]


def get_bad_repos(fusion_path: str) -> List[str]:
    """Filters repositories which have issues running git commands"""
    return [
        repo
        for repo in os.listdir(fusion_path)
        if not test_repo(os.path.join(fusion_path, repo))
    ]


def get_commit_date(git_repo: Git, commit: str) -> datetime:
    """Gets the date when a commit was made"""
    commit_date: str = git_repo.show(
        '-s',
        '--pretty=%aI',
        commit
    )
    return datetime.fromisoformat(commit_date)


def get_commit_files(git_repo: Git, commit: str) -> List[str]:
    """Gets a list of files modified in a certain commit"""
    files: str = git_repo.show(
        '--name-only',
        '--pretty=format:',
        commit
    )
    return files.split('\n')


def get_commit_hunks(repo_path: str, commit: str) -> int:
    metric = HunksCount(
        path_to_repo=repo_path,
        from_commit=commit,
        to_commit=commit
    )
    files = metric.count()
    hunks = sum(files.values())
    return hunks


def get_commit_stats(git_repo: Git, commit: str) -> str:
    """Returns the amount of changed lines a commit has"""
    stats: str = git_repo.show(
        '--shortstat',
        '--pretty=format:',
        commit
    )
    return stats


def get_git_log_metrics(
    git_repo: Git,
    file: str,
    metrics: List[str]
) -> Dict[str, List[str]]:
    """Fetches multiple metrics in one git log command"""
    git_metrics: Dict[str, List[str]] = {}
    metrics_git_format: str = translate_metrics_to_git_format(metrics)
    try:
        if 'stats' in metrics:
            git_log = git_repo.log(
                '--no-merges',
                '--follow',
                '--shortstat',
                f'--pretty={metrics_git_format}',
                file
            ).replace('\n\n ', ',').replace(', ', '--').split('\n')
        else:
            git_log = git_repo.log(
                '--no-merges',
                '--follow',
                f'--pretty={metrics_git_format}',
                file
            ).split('\n')
        for idx, metric in enumerate(metrics):
            metric_log: List[str] = []
            for record in git_log:
                metric_log.append(record.split(',')[idx])
            git_metrics.update({metric: metric_log})
    except (
        GitCommandError,
        GitCommandNotFound,
    ):
        # Triggered when searching for a file that does not exist in the
        # version current
        pass
    return git_metrics


def get_file_authors_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the author of every commit that modified a file"""
    author_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%ae',
        file
    )
    return author_history.split('\n')


def get_file_commit_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the hashes of the commits that touched a file"""
    commit_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%H',
        file
    )
    return commit_history.split('\n')


def get_file_date_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with dates in ISO format of every commit the file has"""
    date_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%aI',
        file
    )
    return date_history.split('\n')


def get_file_stat_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the amount of changed lines each commit has"""
    stat_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--shortstat',
        '--pretty=',
        file
    )
    return stat_history.split('\n')


def get_latest_commits(git_repo: Git, since: str) -> List[str]:
    """Gets the list of commits made to a repository since the defined date"""
    latest_commits: str = git_repo.log(
        '--no-merges',
        '--pretty=%H',
        f'--since="{since}"'
    )
    return latest_commits.split('\n')


def get_log_file_metrics(
    logs_dir: str,
    repo: str,
    file: str
) -> GitMetrics:
    """Read the log file and extract the author, hash, date and diff"""
    git_metrics: GitMetrics = GitMetrics(
        author_email=[],
        commit_hash=[],
        date_iso_format=[],
        stats=[]
    )
    cursor: str = ''
    with open(os.path.join(logs_dir, f'{repo}.log'), 'r') as log_file:
        for line in log_file:
            # An empty line marks the start of a new commit diff
            if not line.strip('\n'):
                cursor = 'info'
                continue
            # Next, there is a line with the format 'Hash,Author,Date'
            if cursor == 'info':
                info: List[str] = line.strip('\n').split(',')
                commit: str = info[0]
                author: str = info[1]
                date: str = info[2]
                cursor = 'diff'
                continue
            # Next, there is a list of changed files and the changed lines
            # with the format 'Additions    Deletions   File'
            if cursor == 'diff':
                changed_name: bool = False
                # Keeps track of the file if its name was changed
                if '=>' in line:
                    match = re.match(
                        RENAME_REGEX,
                        line.strip('\n').split('\t')[2]
                    )
                    if match:
                        path_info: Dict[str, str] = match.groupdict()
                        if file == (
                            f'{path_info["pre_path"]}{path_info["new_name"]}'
                            f'{path_info["post_path"]}'
                        ):
                            changed_name = True
                            file = (
                                f'{path_info["pre_path"]}'
                                f'{path_info["old_name"]}'
                                f'{path_info["post_path"]}'
                            )
                if file in line or changed_name:
                    git_metrics['author_email'].append(author)
                    git_metrics['commit_hash'].append(commit)
                    git_metrics['date_iso_format'].append(date)

                    stats: List[str] = line.strip('\n').split('\t')
                    git_metrics['stats'].append(
                        f'1 file changed, {stats[0]} insertions (+), '
                        f'{stats[1]} deletions (-)'
                    )
    return git_metrics


def get_repository_commit_history(git_repo: Git) -> List[str]:
    """Gets the complete commit history of a git repository"""
    commit_history: str = git_repo.log('--no-merges', '--pretty=%H')
    return commit_history.split('\n')


def get_repositories_log(dir_: str, repos_paths: ndarray) -> None:
    """Gets the complete log of the repositories and saves them to files"""
    for repo_path in repos_paths:
        repo: str = os.path.basename(repo_path)
        try:
            git_repo: Git = git.Git(repo_path)
            git_log: str = git_repo.log(
                '--no-merges',
                '--numstat',
                '--pretty=%n%H,%ae,%aI%n'
            ).replace('\n\n\n', '\n')
            with open(os.path.join(dir_, f'{repo}.log'), 'w') as log_file:
                log_file.write(git_log)
        except GitCommandNotFound as exc:
            log_exception('info', exc, message=f'Repo {repo} does not exist')


def get_repository_files(repo_path: str) -> List[str]:
    """Lists all the files inside a repository relative to the repository"""
    ignore_dirs: List[str] = ['.git']
    return [
        os.path.join(path, filename).replace(
            f'{os.path.dirname(repo_path)}/',
            ''
        )
        for path, _, files in os.walk(repo_path)
        for filename in files
        if all([dir_ not in path for dir_ in ignore_dirs])
    ]


def parse_git_shortstat(stat: str) -> Tuple[int, int]:
    insertions: int = 0
    deletions: int = 0
    match = re.match(STAT_REGEX, stat.strip())
    if match:
        groups: Dict[str, str] = match.groupdict()
        if groups['insertions']:
            insertions = int(groups['insertions'])
        if groups['deletions']:
            deletions = int(groups['deletions'])
    return insertions, deletions


def test_repo(repo_path: str) -> bool:
    """Checks correct configuration of a repository by running `git log`"""
    git_repo: Git = git.Git(repo_path)
    is_repo_ok: bool = True
    try:
        git_repo.log()
    except GitCommandError:
        is_repo_ok = False
    return is_repo_ok


def translate_metrics_to_git_format(metrics: List[str]) -> str:
    """Translates metrics to the format used by git pretty print"""
    metrics_dict: Dict[str, str] = {
        'commit_hash': '%H',
        'author_email': '%ae',
        'date_iso_format': '%aI'
    }
    metric_git_format: str = ','.join([
        metrics_dict[metric]
        for metric in metrics
        if metrics_dict.get(metric)
    ])
    return metric_git_format
