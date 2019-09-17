# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud.gcp packages."""

# standard imports
import os
import tempfile
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.gcp import project


# Constants
GOOGLE_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT']
GOOGLE_CREDENTIALS_BAD = "bad"
PROJECT_ID = 'vital-pillar-253219'


#
# Helpers
#


def write_good_gcp_creds_file() -> str:
    """Create GCP credentials file."""
    _, path = tempfile.mkstemp()
    with open(path, 'w+') as cred_fd:
        cred_fd.write(GOOGLE_CREDENTIALS)
    return path


def write_bad_gcp_creds_file() -> str:
    """Create GCP credentials file."""
    _, path = tempfile.mkstemp()
    with open(path, 'w+') as cred_fd:
        cred_fd.write(GOOGLE_CREDENTIALS_BAD)
    return path


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)


#
# Open tests
#


def test_gmail_users_open():
    """Check if there are gmail users in project."""
    path = write_good_gcp_creds_file()
    assert project.has_gmail_users(project_id=PROJECT_ID, cred_file=path)

#
# Closing tests
#


def test_gmail_users_close():
    """Check if there are gmail users in project."""
    path = write_bad_gcp_creds_file()
    assert project.has_gmail_users(project_id=PROJECT_ID,
                                   cred_file=path).is_unknown()

    with no_connection():
        assert project.has_gmail_users(project_id=PROJECT_ID,
                                       cred_file=path).is_unknown()
