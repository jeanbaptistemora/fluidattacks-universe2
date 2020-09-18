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
import toolbox
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
    assert not response.ok


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

@pytest.mark.skip(reason="Pending to fix")
def test_integrates_mutations_approve_vulnerability():
    """Test integrates mutations."""
    uuid = str(uuid4())
    response = integrates.Mutations.approve_vulns(
        API_TOKEN, FINDING, uuid, approval_status=False)
    assert response.ok
    assert not response.data['approveVulnerability']['success']


def test_integrates_mutations_upload_file():
    """Test integrates mutations."""
    now_str: str = str(datetime.datetime.utcnow())
    content = f"""
        inputs:
        - url: 'https://{now_str}'
          field: 'test'
          state: open
        lines:
        - path: 'Test/{now_str}'
          line: '1'
          state: open
        """

    with toolbox.utils.file.create_ephemeral('vulns.yaml', content) as file:
        response = integrates.Mutations.upload_file(API_TOKEN, FINDING, file)
        assert response.ok


def test_integrates_mutations_update_evidence():
    now_str: str = str(datetime.datetime.utcnow())
    content: str = f"""
        #! /usr/bin/env asserts
        # {now_str}

        from fluidasserts.db import postgresql

        postgresql.has_not_data_checksums_enabled(
            dbname,
            user, password,
            host, port,
        )
        """

    with toolbox.utils.file.create_ephemeral('exploit.exp', content) as file:
        response = integrates.Mutations.update_evidence(
            API_TOKEN, FINDING, 'EXPLOIT', file)

        assert response.ok
