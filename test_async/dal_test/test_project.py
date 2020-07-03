import pytest
from django.test import TestCase

from backend.dal.project import (
    get_current_month_information, get_pending_verification_findings,
    list_internal_managers, list_project_managers, update_access, get_users
)


@pytest.mark.skip(
    reason="https://gitlab.com/fluidattacks/integrates/issues/1913")
def test_get_current_month_information():
    """makes sure that we are getting the info properly"""
    project_name = 'unittesting'
    query_authors = '''SELECT COUNT(DISTINCT(
        Commits.author_name || '_' || Commits.author_email))
        FROM git.commits AS "Commits"
        WHERE (Commits.subscription = %s AND
            (Commits.integration_authored_at BETWEEN %s AND %s));'''
    query_commits = '''SELECT COUNT(Commits.sha1)
        FROM git.commits AS "Commits"
        WHERE (Commits.subscription = %s AND
            (Commits.authored_at BETWEEN %s AND %s))
        LIMIT 100000;'''
    assert get_current_month_information(
        project_name, query_authors) is not None
    assert get_current_month_information(
        project_name, query_commits) is not None

async def test_get_pending_verification_findings():
    project_name = 'unittesting'
    findings = await get_pending_verification_findings(project_name)
    assert len(findings) >= 1
    assert 'finding' in findings[0]
    assert 'finding_id' in findings[0]
    assert 'project_name' in findings[0]

def test_list_internal_managers():
    assert list_internal_managers('oneshottest') == []

    assert list_internal_managers('unittesting') == \
        ['unittest2@fluidattacks.com']

def test_update_access():
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', False)
    assert update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', True)
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', True)
    assert update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', False)
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', False)
