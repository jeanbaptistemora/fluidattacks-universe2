# Standar library
import re
from contextlib import suppress
from typing import (Dict)

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
    re.compile(r'^.*visualstudio.com/.*/_git/(.*)$'),
    # https://xxx@gitlab.com/xxx/repo_name.git
    re.compile(r'^.*(?:gitlab|github).com(?::|\/).*\/(.*).git$'),
]


def get_repository_metadata(repo_path: str = '.') -> Dict[str, str]:
    git_branch = DEFAULT_COLUMN_VALUE
    git_commit = DEFAULT_COLUMN_VALUE
    git_commit_author = DEFAULT_COLUMN_VALUE
    git_commit_authored_date = DEFAULT_COLUMN_VALUE
    git_repo = DEFAULT_COLUMN_VALUE
    git_origin = DEFAULT_COLUMN_VALUE

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

        git_repo = DEFAULT_COLUMN_VALUE
        origins = []
        with suppress(ValueError):
            origins = list(repo.remote().urls)
        git_origin = DEFAULT_COLUMN_VALUE
        if origins:
            git_origin = origins[0]
            for regex in REGEXES_GIT_REPO_FROM_ORIGIN:
                match = regex.match(git_origin)
                if match and match.group(1):
                    git_repo = match.group(1)

    return {
        'git_branch': git_branch,
        'git_commit': git_commit,
        'git_commit_author': git_commit_author,
        'git_commit_authored_date': git_commit_authored_date,
        'git_repo': git_repo,
        'git_origin': git_origin
    }
