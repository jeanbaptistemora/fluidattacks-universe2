# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.proto.git."""

# standard imports
# None

# 3rd party imports
from fluidasserts.proto import git
import pytest
pytestmark = pytest.mark.asserts_module('proto_git')

# local imports


# Constants

COMMIT_ID = 'aaf0312e43ed7637c69af34bba59897f0e0810f8'
BAD_COMMIT_ID = '123123'
REPO_PATH = '.'
REPO_SUB_DIR = 'test/'
REPO_OPEN = 'test/static/git/open'
REPO_CLOSE = 'test/static/git/close'
REPO_NOT_FOUND = 'test/static/git/not_found'

#
# Open tests
#


def test_commit_has_secret_open():
    """Commit has secret?."""
    assert git.commit_has_secret(REPO_PATH, COMMIT_ID, 'CaselessKeyword')


def test_has_insecure_gitignore_open():
    """Commit has insecure .gitignore?."""
    assert git.has_insecure_gitignore(REPO_OPEN)
#
# Closing tests
#


def test_commit_has_secret_close():
    """Commit has secret?."""
    assert not git.commit_has_secret(REPO_PATH, BAD_COMMIT_ID,
                                     'CaselessKeyword')
    assert not git.commit_has_secret(REPO_PATH, COMMIT_ID, 'NotFoundString')
    # Git python needs the top level of the repo
    #   if you pass a submodule it raises git.exc.InvalidGitRepositoryError
    assert not git.commit_has_secret(REPO_SUB_DIR, COMMIT_ID, 'NotFoundString')


def test_has_insecure_gitignore_close():
    """Commit has insecure .gitignore?."""
    assert not git.has_insecure_gitignore(REPO_CLOSE)
    assert not git.has_insecure_gitignore(REPO_NOT_FOUND)

def test_has_secret_in_git_history_open():
    """Git history has secret."""
    assert git.has_secret_in_git_history(
        '.', 'test/static/lang/java/GenericExceptionsOpen.java',
        'Q68+KUykdS_v+Tc%').is_open()

def test_has_secret_in_git_history_closed():
    """Git history has secret."""
    assert git.has_secret_in_git_history(
        '.', 'test/static/lang/java/GenericExceptionsClose.java',
        'Q68+KUykdS_v+Tc%').is_closed()