import pytest
from django.test import TestCase

from backend.dal.project import (
    get_current_month_information, get_pending_verification_findings
)


class ProjectTests(TestCase):

    @pytest.mark.skip(
        reason="https://gitlab.com/fluidattacks/integrates/issues/1913")
    def test_get_current_month_information(self):
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

    def test_get_pending_verification_findings(self):
        project_name = 'unittesting'
        findings = get_pending_verification_findings(project_name)
        assert len(findings) >= 1
        assert 'finding' in findings[0]
        assert 'finding_id' in findings[0]
        assert 'project_name' in findings[0]
