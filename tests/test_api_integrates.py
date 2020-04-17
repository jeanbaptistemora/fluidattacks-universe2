# Standard library
from uuid import uuid4
import os
import datetime
import tempfile
import textwrap
from aiohttp.client_exceptions import ContentTypeError

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
    with pytest.raises(ContentTypeError):
        response = integrates.Queries.me(API_TOKEN_BAD * 1000)


def test_integrates_queries_project():
    """Test integrates queries."""
    # This will guarantee that we have always our fields updated
    #   if this query fails then integrates has changed,
    #   please update ALL our queries
    response = integrates.Queries.project(
        api_token=API_TOKEN,
        project_name=PROJECT,
        with_drafts=True,
        with_findings=True)
    assert response.ok


def test_integrates_queries_finding():
    """Test integrates queries."""
    # This will guarantee that we have always our fields updated
    #   if this query fails then integrates has changed,
    #   please update ALL our queries
    response = integrates.Queries.finding(
        api_token=API_TOKEN,
        identifier=FINDING,
        with_vulns=True)
    assert response.ok


def test_integrates_queries_resources():
    """Test integrates queries."""
    # This will guarantee that we have always our fields updated
    #   if this query fails then integrates has changed,
    #   please update ALL our queries
    response = integrates.Queries.resources(
        api_token=API_TOKEN,
        project_name=PROJECT)
    assert response.ok


def test_integrates_mutations_update_access_token():
    """Test integrates mutations."""
    response = integrates.Mutations.update_access_token(API_TOKEN_BAD, 0)
    assert not response.ok


def test_integrates_mutations_invalidate_access_token():
    """Test integrates mutations."""
    response = integrates.Mutations.invalidate_access_token(API_TOKEN_BAD)
    assert not response.ok


def test_integrates_mutations_approve_vulnerability():
    """Test integrates mutations."""
    uuid = str(uuid4())
    response = integrates.Mutations.approve_vulns(
        API_TOKEN, FINDING, uuid, approval_status=False)
    assert response.ok
    assert not response.data['approveVulnerability']['success']


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
