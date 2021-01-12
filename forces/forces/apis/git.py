# Standar library
import os
import re
from contextlib import suppress
from typing import (
    Dict,
    Optional,
)

# Third libraries
import pytz
from git import (
    InvalidGitRepositoryError,
    Repo,
    Commit,
)

# Contants
DEFAULT_COLUMN_VALUE: str = 'unable to retrieve'
REGEXES_GIT_REPO_FROM_ORIGIN = [
    # https://xxxx.visualstudio.com/xxx/_git/repo_name
    re.compile(r'^.*visualstudio.com\/.*\/_git\/(.*)$'),
    # git@ssh.dev.azure.com:v3/xxx/repo_name
    re.compile(r'^.*azure.com:.*\/(.*)'),
    # git@bitbucket.org:xxxxx/repo_name
    re.compile(r'^.*bitbucket.org:.*\/(.*)'),
    # https://xxx@gitlab.com/xxx/repo_name.git
    re.compile(r'^.*(?:gitlab|github).com(?::|\/).*\/(.*?)(?:\.git)?$'),
]


def get_repo_name_from_vars() -> Optional[str]:
    common_names = {
        'BUILD_REPOSITORY_NAME',  # Azure devops
        'CI_PROJECT_NAME',  # gitlab-ci
        'CIRCLE_PROJECT_REPONAME',  # circleci
    }
    for var in common_names:
        if name := os.environ.get(var):
            return name
    return None


def extract_repo_name(pattern: str) -> Optional[str]:
    for regex in REGEXES_GIT_REPO_FROM_ORIGIN:
        match = regex.match(pattern)
        if match and match.group(1):
            return match.group(1)

    return None


def get_repository_metadata(repo_path: str = '.') -> Dict[str, str]:
    git_branch = DEFAULT_COLUMN_VALUE
    git_commit = DEFAULT_COLUMN_VALUE
    git_commit_author = DEFAULT_COLUMN_VALUE
    git_commit_authored_date = DEFAULT_COLUMN_VALUE
    git_origin = DEFAULT_COLUMN_VALUE
    git_repo = DEFAULT_COLUMN_VALUE

    with suppress(InvalidGitRepositoryError):
        repo = Repo(repo_path, search_parent_directories=True)
        head_commit: Commit = repo.head.commit

        git_branch = DEFAULT_COLUMN_VALUE
        with suppress(TypeError):
            git_branch = repo.active_branch.name

        git_commit = head_commit.hexsha
        git_commit_author = (f'{head_commit.author.name}'
                             f' <{head_commit.author.email}>')
        git_commit_authored_date = head_commit.authored_datetime.astimezone(
            pytz.UTC).isoformat()

        origins = list(repo.remote().urls)
        with suppress(IndexError):
            git_origin = origins[0]

        if name := get_repo_name_from_vars():
            git_repo = name
        elif name := extract_repo_name(git_origin):
            git_repo = name
        elif git_repo == DEFAULT_COLUMN_VALUE:
            with suppress(IndexError):
                git_repo = os.path.basename(os.path.split(repo.git_dir)[0])
    return {
        'git_branch': git_branch,
        'git_commit': git_commit,
        'git_commit_author': git_commit_author,
        'git_commit_authored_date': git_commit_authored_date,
        'git_repo': git_repo,
        'git_origin': git_origin
    }
