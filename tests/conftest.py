# Standard library
import os
import sys
import shlex
import contextlib

# Third parties libraries
import pytest
import unittest.mock

# Local libraries
import toolbox.toolbox
from toolbox import logger
from toolbox import resources

# Constants
SUBS: str = 'continuoustest'


@contextlib.contextmanager
def _relocate(path: str = '../'):
    """Change temporarily the working directory."""
    # The toolbox need to be run in the root of the repository
    current_dir: str = os.getcwd()
    try:
        os.chdir(path)
        logger.info('yield', os.getcwd())
        yield os.getcwd()
    finally:
        # Return to where we were
        logger.info('finally', current_dir)
        os.chdir(current_dir)


@pytest.fixture(scope='function')
def relocate(request):
    """Change temporarily the working directory."""
    with _relocate() as new_path:
        yield new_path


@pytest.fixture(scope='function')
def relocate_to_cloned_repo(request):
    """Change temporarily the working directory."""
    with _relocate(path=f'../subscriptions/{SUBS}/fusion/continuous') as new_path:
        yield new_path


@pytest.fixture(scope='session', autouse=True)
def prepare(request):
    """Prepare the environment by cloning the test repository."""
    with _relocate():
        assert resources.repo_cloning(SUBS)
