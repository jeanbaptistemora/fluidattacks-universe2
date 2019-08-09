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


class GraphQLTests(TestCase):

    def test_get_alert(self):
        """Check for project alert"""
        query = '''{
            alert(projectName:"unittesting", organization:"fluid"){
                message
            }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        if 'alert' in result.data:
            message = result.data['alert']['message']
            assert message == 'unittest'
        assert 'alert' in result.data

    def test_get_event(self):
        """Check for eventuality"""
        query = '''{
            event(identifier:"418900971"){
                detail
            }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = dict(SCHEMA.execute(query, context_value=request).data)
        if 'event' in result.keys():
            detail = dict(result['event'])['detail']
            assert detail == 'Integrates unit test'
        assert 'event' in result

    def test_get_events(self):
        """Check for eventualities"""
        query = '''{
            events(projectName:"unittesting"){
                detail
            }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = dict(SCHEMA.execute(query, context_value=request).data)
        if 'events' in result:
            detail = dict(result['events'][0])['detail']
            assert len(detail) >= 1
        assert 'events' in result

    def test_get_finding(self):
        """ Check for finding """
        query = '''{
          finding(identifier: "422286126"){
            id
            vulnerabilities {
                findingId
                id
                historicState
                specific
                vulnType
                where
            }
          }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('finding')['id'] == '422286126'
        test_data = OrderedDict([
            ('findingId', '422286126'),
            ('id', u'80d6a69f-a376-46be-98cd-2fdedcffdcc0'),
            ('historicState',
             [{u'date': u'2018-09-28 10:32:58', u'state': u'open'},
              {u'date': u'2019-01-08 16:01:26', u'state': u'open'}]),
            ('specific', u'phone'),
            ('vulnType', u'inputs'),
            ('where', u'https://example.com')])
        assert test_data in result.data.get('finding')['vulnerabilities']

    def test_get_vulnerability(self):
        """Check for vulnerabilities"""
        query = '''
            query {
                finding(identifier: "422286126") {
                id
                releaseDate
                portsVulns: vulnerabilities(
                    vulnType: "ports") {
                    ...vulnInfo
                }
                linesVulns: vulnerabilities(
                    vulnType: "lines") {
                    ...vulnInfo
                }
                inputsVulns: vulnerabilities(
                    vulnType: "inputs") {
                    ...vulnInfo
                }
                }
            }
            fragment vulnInfo on Vulnerability {
                vulnType
                where
                specific
                currentState
                id
                findingId
                treatment
                treatmentManager
                treatmentJustification
                externalBts
            }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('finding')['id'] == '422286126'
        test_data = OrderedDict([
            ('vulnType', u'inputs'),
            ('where', u'https://example.com'),
            ('specific', u'phone'),
            ('currentState', u'open'),
            ('id', u'80d6a69f-a376-46be-98cd-2fdedcffdcc0'),
            ('findingId', '422286126'),
            ('treatment', u'In progress'),
            ('treatmentManager', u'continuoushacking@gmail.com'),
            ('treatmentJustification', u'Test 123'),
            ('externalBts', '')])
        assert test_data in result.data.get('finding')['inputsVulns']

    def test_get_resources(self):
        """ Check for project resources """
        query = '''{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert 'https://gitlab.com/fluidsignal/engineering/' in \
               result.data.get('resources')['repositories']
        assert 'https://fluidattacks.com/' in \
               result.data.get('resources')['environments']

    def test_add_resources(self):
        """ Check for add project resources"""
        repos_to_add = [
            {'branch': 'master',
             'urlRepo': 'https://gitlab.com/fluidsignal/unittest'}
        ]
        envs_to_add = [
            {'urlEnv': 'https://unittesting.fluidattacks.com/'},
        ]
        query = '''mutation {
          addRepositories(
            projectName: "unittesting", resourcesData: "$repos") {
            success
          }
          addEnvironments(projectName: "unittesting", resourcesData: "$envs") {
            success
          }
        }'''
        query = query.replace(
            '$repos', json.dumps(repos_to_add).replace('"', '\\"'))
        query = query.replace(
            '$envs', json.dumps(envs_to_add).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('addRepositories')['success']
        assert result.data.get('addEnvironments')['success']

    def test_remove_vulnerability(self):
        """check for remove_vulnerability"""
        test_client = Client(SCHEMA)
        query = '''
            mutation{
                deleteVulnerability (
                id: "39db67dd-dec8-4957-b9c0-fc5a6f2aee03"
                findingId: "475041513"
                ) {
                success
                }
            }
        '''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = test_client.execute(query, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['deleteVulnerability']

    def test_remove_resources(self):
        """ Check for remove project resources """
        repo_to_remove = {
            'branch': 'master',
            'urlRepo': 'https://gitlab.com/fluidsignal/unittest'}
        env_to_remove = {'urlEnv': 'https://unittesting.fluidattacks.com/'}
        query = '''mutation{
          removeRepositories(
            projectName: "unittesting", repositoryData: "$repo"){
            success
          }
          removeEnvironments(
            projectName: "unittesting", repositoryData: "$env"){
            success
          }
        }'''
        query = query.replace(
            '$repo', json.dumps(repo_to_remove).replace('"', '\\"'))
        query = query.replace(
            '$env', json.dumps(env_to_remove).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('removeRepositories')['success']
        assert result.data.get('removeEnvironments')['success']

    def test_update_treatment_vuln(self):
        """test update_treatment_vuln """
        testing_client = Client(SCHEMA)
        query = '''
            mutation {
                updateTreatmentVuln (
                data: {
                        btsUrl: "https://www.google.com/",
                        findingId: "463462578",
                        treatment: "accepted",
                        treatmentJustification:
                            "Will be solved the next sprint."
                        treatmentManager: "test.test@test.test"
                        vulnerabilities:
                            ["ea9c6026-c98d-4b5f-ba0c-54caf8a586a8"]
                        }
                findingId: "463462578"
                ){
                success
                }
            }
        '''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['updateTreatmentVuln']

    def test_grant_user_access(self):
        testing_client = Client(SCHEMA)
        query = '''
            mutation {
                grantUserAccess (
                email: "test@test.test",
                organization: "test",
                phoneNumber: "3453453453"
                projectName: "unittesting",
                responsibility: "test",
                role: "customer") {
                success
                grantedUser {
                    email
                    role
                    responsibility
                    phoneNumber
                    organization
                    firstLogin
                    lastLogin
                }
                }
            }
        '''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantUserAccess']

    def test_get_user(self):
        query = '''
            query {
                userData(projectName: "unittesting",
                         userEmail: "continuoushacking@gmail.com") {
                    organization
                    responsibility
                    phoneNumber
                }
            }
        '''
        testing_client = Client(SCHEMA)
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context_value=request)
        print result
        assert 'errors' not in result
        assert 'userData' in result['data']

    def test_upload_files(self):
        file_to_upload = NamedTemporaryFile()
        with file_to_upload.file as test_file:
            file_data = [
                {'description': 'test',
                 'fileName': file_to_upload.name.split('/')[2],
                 'uploadDate': ''}
            ]
            query = '''
            mutation {
            addFiles (
                filesData: "$fileData",
                projectName: "UNITTESTING") {
                success
                resources {
                environments
                files
                repositories
                }
            }
            }
            '''
            query = query.replace(
                '$fileData', json.dumps(file_data).replace('"', '\\"'))
            testing_client = Client(SCHEMA)
            request = RequestFactory().get('/')
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()
            request.session['username'] = 'unittest'
            request.session['company'] = 'unittest'
            request.session['role'] = 'admin'
            request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
                {
                    'user_email': 'unittest',
                    'user_role': 'admin',
                    'company': 'unittest'
                },
                algorithm='HS512',
                key=settings.JWT_SECRET,
            )
            request.FILES['document'] = File(test_file)
            result = testing_client.execute(query, context_value=request)
            assert 'errors' not in result
            assert 'success' in result['data']['addFiles']

    def test_add_user(self):
        query = '''
            mutation {
              grantUserAccess (
                email: "test@test.test",
                organization: "test",
                phoneNumber: "7357",
                projectName: "test",
                responsibility: "test",
                  role: "customer") {
                    success
                      grantedUser {
                        email
                        role
                        responsibility
                        phoneNumber
                        organization
                        firstLogin
                        lastLogin
                    }
                }
            }
        '''
        testing_client = Client(SCHEMA)
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = testing_client.execute(query, context_value=request)
        assert 'errors' not in result
        assert 'success' in result['data']['grantUserAccess']


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
