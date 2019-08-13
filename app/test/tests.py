import json
from collections import OrderedDict
from decimal import Decimal
from tempfile import NamedTemporaryFile

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.core.files import File
from graphql.error import GraphQLError
from graphene.test import Client
from jose import jwt

from app.api.schema import SCHEMA
from app.dal.helpers.formstack import FormstackAPI
from app.dal.project import get_current_month_information
from app.dto.finding import FindingDTO
from app.entity.user import (validate_email_address,
                             validate_field,
                             validate_phone_field)
from app.utils import cvss


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class FormstackAPITests(TestCase):
    def test_request(self):
        """ Make a request to formstack and verify that
            the key data exists in the response json. """
        api_frms = FormstackAPI()
        url = 'https://www.formstack.com/api/v2/submission/293276999.json'
        request = api_frms.request('GET', url)
        assert 'data' in request

    def test_get_submission(self):
        """ Check that Formstack correctly return a submission query. """
        api_frms = FormstackAPI()
        submission_id = '293276999'
        request = api_frms.get_submission(submission_id)
        assert request['id'] == submission_id

    def test_get_findings(self):
        """Check that Formstack correctly return the findings of a project."""
        api_frms = FormstackAPI()
        project = 'basaiti'
        request = api_frms.get_findings(project)
        assert 'submissions' in request

    def test_get_eventualities(self):
        """ Check that Formstack correctly return
            the eventualities of a project. """
        api_frms = FormstackAPI()
        project = 'basaiti'
        request = api_frms.get_eventualities(project)
        assert 'submissions' in request

    def test_update_eventuality(self):
        """Check that an eventuality update request works correctly."""
        api_frms = FormstackAPI()
        affectation = '0'
        submission_id = '244210431'
        data = {
            '29042542': affectation
        }
        request = api_frms.update(submission_id, data)
        assert 'success' in request


class cvssTests(TestCase):

    def test_calculate_cvss2_basescore(self):
        severity = {'confidentialityImpact': 0, 'integrityImpact': 0.275,
                    'availabilityImpact': 0, 'accessComplexity': 0.61,
                    'authentication': 0.704, 'accessVector': 1
                    }
        fin_dto = FindingDTO()
        cvss_version = '2'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS_PARAMETERS, cvss_version)
        cvss_basescore_test = Decimal(4.3).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    def test_calculate_cvss2_temporal(self):
        severity = {'confidentialityImpact': 0, 'integrityImpact': 0.275,
                    'availabilityImpact': 0, 'accessComplexity': 0.61,
                    'authentication': 0.704, 'accessVector': 1,
                    'exploitability': 0.95, 'resolutionLevel': 0.95,
                    'confidenceLevel': 0.95
                    }
        fin_dto = FindingDTO()
        cvss_version = '2'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS_PARAMETERS, cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, cvss_basescore, cvss_version)
        cvss_temporal_test = Decimal(3.7).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    def test_calculate_cvss2_environment(self):
        severity = {'accessComplexity': 0.61, 'authentication': 0.704,
                    'accessVector': 1, 'confidentialityImpact': 0,
                    'confidentialityRequirement': 0.5, 'confidenceLevel': 0.95,
                    'integrityRequirement': 0.5, 'availabilityImpact': 0,
                    'availabilityRequirement': 0.5, 'findingDistribution': 0.25,
                    'resolutionLevel': 0.95, 'integrityImpact': 0.275,
                    'collateralDamagePotential': 0.1, 'exploitability': 0.95,
                    }
        fin_dto = FindingDTO()
        cvss_version = '2'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, fin_dto.CVSS_PARAMETERS, cvss_version)
        cvss_environment_test = Decimal(0.9).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test

    def test_calculate_cvss3_scope_changed_basescore(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 1,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.68, 'userInteraction': 0.85
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_basescore_test = Decimal(6.4).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    def test_calculate_cvss3_scope_unchanged_basescore(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 0,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.62, 'userInteraction': 0.85
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_basescore_test = Decimal(5.4).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    def test_calculate_cvss3_scope_changed_temporal(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 1,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.68, 'userInteraction': 0.85,
                    'exploitability': 0.97, 'remediationLevel': 0.97,
                    'reportConfidence': 1
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, float(cvss_basescore), cvss_version)
        cvss_temporal_test = Decimal(6.1).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    def test_calculate_cvss3_scope_unchanged_temporal(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 0,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.62, 'userInteraction': 0.85,
                    'exploitability': 0.97, 'remediationLevel': 0.97,
                    'reportConfidence': 1
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, float(cvss_basescore), cvss_version)
        cvss_temporal_test = Decimal(5.1).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    def test_calculate_cvss3_scope_changed_environment(self):
        severity = {'modifiedConfidentialityImpact': 0.22, 'reportConfidence': 1,
                    'modifiedIntegrityImpact': 0.22, 'modifiedAvailabilityImpact': 0.22,
                    'confidentialityRequirement': 0.5, 'integrityRequirement': 0.5,
                    'availabilityRequirement': 0.5, 'modifiedSeverityScope': 1,
                    'modifiedAttackVector': 0.85, 'modifiedAttackComplexity': 0.77,
                    'modifiedPrivilegesRequired': 0.68, 'remediationLevel': 0.97,
                    'exploitability': 0.97, 'modifiedUserInteraction': 0.85
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_environment_test = Decimal(5.3).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test

    def test_calculate_cvss3_scope_unchanged_environment(self):
        severity = {'modifiedConfidentialityImpact': 0.22, 'reportConfidence': 1,
                    'modifiedIntegrityImpact': 0.22, 'modifiedAvailabilityImpact': 0.22,
                    'confidentialityRequirement': 0.5, 'integrityRequirement': 0.5,
                    'availabilityRequirement': 0.5, 'modifiedSeverityScope': 0,
                    'modifiedAttackVector': 0.85, 'modifiedAttackComplexity': 0.77,
                    'modifiedPrivilegesRequired': 0.62, 'remediationLevel': 0.97,
                    'exploitability': 0.97, 'modifiedUserInteraction': 0.85
                    }
        fin_dto = FindingDTO()
        cvss_version = '3'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, fin_dto.CVSS3_PARAMETERS, cvss_version)
        cvss_environment_test = Decimal(4.6).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test


class ValidationTests(TestCase):

    def test_validate_email_address(self):
        """makes sure that the email is being validated properly"""
        assert validate_email_address('test@test.test')
        assert validate_email_address('test.test@test.test')
        assert validate_email_address('test.test@test.test.test')
        with pytest.raises(GraphQLError):
            assert validate_email_address('test@test')
        with pytest.raises(GraphQLError):
            assert validate_email_address('test')

    def test_validate_field(self):
        """makes sure that the  field is filtering only = sign at start"""
        assert validate_field('t35t 7 test @ test')
        with pytest.raises(GraphQLError):
            assert validate_field('=test')

    def test_validate_phone_number(self):
        assert validate_phone_field("123123123")
        with pytest.raises(GraphQLError):
            assert validate_phone_field("asdasdasd")
        with pytest.raises(GraphQLError):
            assert validate_phone_field("=12123123123")


class bdAccessTests(TestCase):

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
