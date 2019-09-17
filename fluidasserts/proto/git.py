# -*- coding: utf-8 -*-

"""This module allows to check GIT vulnerabilities."""

# standard imports
import os

# third party imports
import git

# local imports
from fluidasserts import SAST, LOW, _get_result_as_tuple_sast
from fluidasserts.utils.decorators import unknown_if, api


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

    return _get_result_as_tuple_sast(
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

    return _get_result_as_tuple_sast(
        path=gitignore_path,
        msg_open='All security entries were found in .gitignore',
        msg_closed='Not all security entries were found in .gitignore',
        open_if=not safe_gitignore)
