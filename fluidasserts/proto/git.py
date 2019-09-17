# -*- coding: utf-8 -*-

"""This module allows to check GIT vulnerabilities."""

# standard imports
import os

# third party imports
import git

# local imports
from fluidasserts import Unit, SAST, LOW, OPEN, CLOSED
from fluidasserts.utils.decorators import unknown_if, api


def _get_result_as_tuple(*,
                         path: str,
                         msg_open: str, msg_closed: str,
                         open_if: bool = None) -> tuple:
    """Return the tuple version of the Result object."""
    unit: Unit = Unit(where=path,
                      specific=[msg_open if open_if else msg_closed])

    if open_if:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, git.GitError)
def commit_has_secret(repo: str, commit_id: str, secret: str) -> tuple:
    r"""
    Check if commit has given secret.

    :param repo: Repository path.
    :param commit_id: Commit to test.
    :param secret: Secret to search.
    """
    diff = git.Repo(repo).git.diff(f'{commit_id}~1..{commit_id}')

    return _get_result_as_tuple(
        path=repo,
        msg_open=f'Secret found in commit {commit_id}',
        msg_closed=f'Secret not found in commit {commit_id}',
        open_if=secret in diff)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, git.GitError)
def has_insecure_gitignore(repo: str) -> tuple:
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

    gitignore_path = os.path.join(repo, '.gitignore')

    with open(gitignore_path) as git_fd:
        content = git_fd.read()

    safe_gitignore = all(x in content for x in secure_entries)

    return _get_result_as_tuple(
        path=gitignore_path,
        msg_open='All security entries were found in .gitignore',
        msg_closed='Not all security entries were found in .gitignore',
        open_if=not safe_gitignore)
