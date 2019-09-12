# -*- coding: utf-8 -*-

"""This module allows to check GIT vulnerabilities."""

# standard imports
import os

# third party imports
import git

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify


@notify
@level('low')
@track
def commit_has_secret(repo: str, commit_id: str, secret: str) -> bool:
    r"""
    Check if commit has given secret.

    :param repo: Repository path.
    :param commit_id: Commit to test.
    :param secret: Secret to search.
    """
    try:
        repo_obj = git.Repo(repo)
        diff = repo_obj.git.diff(f'{commit_id}~1..{commit_id}')
    except git.GitError as exc:
        show_unknown('There was an error',
                     details=dict(repo=repo, commit_id=commit_id,
                                  error=str(exc).replace(':', ',')))
        return False

    result = True
    if secret in diff:
        show_open('Secret found in commit',
                  details=dict(repo=repo, commit_id=commit_id,
                               secret=secret))
    else:
        show_close('Secret not found in commit',
                   details=dict(repo=repo, commit_id=commit_id,
                                secret=secret))
        result = False
    return result


@notify
@level('low')
@track
def has_insecure_gitignore(repo: str) -> bool:
    r"""
    Check if .gitignore file has secure exceptions.

    :param repo: Repository path.
    """
    secure_entries = (
        '*.pem',
        '*.key',
        '*.p12',
        'Thumbs.db',
        '.DS_Store',
    )
    result = True
    try:
        with open(os.path.join(repo, '.gitignore')) as git_fd:
            content = git_fd.read()
            result = not all(x in content for x in secure_entries)
    except FileNotFoundError as exc:
        show_unknown('There was an error',
                     details=dict(repo=repo,
                                  error=str(exc).replace(':', ',')))
        return False
    else:
        if result:
            show_open('Security entries not found in .gitignore',
                      details=dict(repo=repo, secure_entries=secure_entries))
        else:
            show_close('Security entries found in .gitignore',
                       details=dict(repo=repo, secure_entries=secure_entries))
        return result
