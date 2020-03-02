# Standard library
import os
import datetime
import tempfile
import textwrap

# Third parties libraries
import pytest

# Local libraries
from toolbox.api import integrates
from toolbox.constants import API_TOKEN

# Constants
FINDING: str = '975673437'
PROJECT: str = 'continuoustest'
API_TOKEN_BAD: str = 'may I join the party guys?'


def test_integrates_queries_me():
    """Test integrates queries."""
    response = integrates.Queries.me(API_TOKEN)
    assert response.ok

    response = integrates.Queries.me(API_TOKEN_BAD)
    assert not response.ok

    # This makes the GraphQL server fail, (too long Authorization header)
    response = integrates.Queries.me(API_TOKEN_BAD * 1000)
    assert response.status_code == 400


def test_integrates_queries_project():
    """Test integrates queries."""
    # This will guarantee that we have always our fields updated
    #   if this query fails then integrates has changed,
    #   please update ALL our queries
    response = integrates.Queries.project(
        api_token=API_TOKEN,
        project_name=PROJECT,
        with_drafts='true',
        with_findings='true')
    assert response.ok


def test_integrates_queries_finding():
    """Test integrates queries."""
    # This will guarantee that we have always our fields updated
    #   if this query fails then integrates has changed,
    #   please update ALL our queries
    response = integrates.Queries.finding(
        api_token=API_TOKEN,
        identifier=FINDING,
        with_vulns='true')
    assert response.ok


def test_integrates_mutations_update_access_token():
    """Test integrates mutations."""
    response = integrates.Mutations.update_access_token(API_TOKEN_BAD, 0)
    assert not response.ok


def test_integrates_mutations_invalidate_access_token():
    """Test integrates mutations."""
    response = integrates.Mutations.invalidate_access_token(API_TOKEN_BAD)
    assert not response.ok


def test_integrates_mutations_upload_file():
    """Test integrates mutations."""
    with tempfile.NamedTemporaryFile(suffix='vulns.yaml') as file:
        now_str: str = str(datetime.datetime.utcnow())
        file.write(textwrap.dedent(f"""
            inputs:
            - url: 'https://{now_str}'
              field: 'test'
              state: open
            lines:
            - path: 'Test/{now_str}'
              line: '1'
              state: open
            """[1:]).encode())
        file.seek(0)

        response = integrates.Mutations.upload_file(
            API_TOKEN, FINDING, file.name)

        assert response.ok
