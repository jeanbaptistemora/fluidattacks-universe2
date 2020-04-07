from tempfile import NamedTemporaryFile
import json
import os

from ariadne import graphql
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from backend.api.schema import SCHEMA

import pytest

pytestmark = pytest.mark.asyncio

class ForcesExecutionsTests(TestCase):

    async def _get_result(self, data):
        """Get result."""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'company': 'unittest',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        _, result = await graphql(SCHEMA, data, context_value=request)
        return result

    async def test_project_name(self):
        """Check for project_name field."""
        query = '''{
          forcesExecutions(projectName: "unittesting"){
            projectName
          }
        }'''
        data = {'query': query}
        result = await self._get_result(data)
        assert 'errors' not in result
        assert result['data']['forcesExecutions']['projectName'] \
            == 'unittesting'

    async def test_executions(self):
        """Check for executions field."""
        query = """
          query {
            forcesExecutions(
                projectName: "unittesting",
                fromDate: "2020-02-01T00:00:00Z",
                toDate: "2020-02-28T23:59:59Z"
            ) {
              executions {
                projectName
                identifier
                date
                exitCode
                gitBranch
                gitCommit
                gitOrigin
                gitRepo
                kind
                log
                strictness
                vulnerabilities {
                  exploits {
                    kind
                    who
                    where
                  }
                  mockedExploits {
                    kind
                    who
                    where
                  }
                  acceptedExploits {
                    kind
                    who
                    where
                  }
                  numOfVulnerabilitiesInExploits
                  numOfVulnerabilitiesInMockedExploits
                  numOfVulnerabilitiesInAcceptedExploits
                }
              }
            }
          }
        """
        data = {'query': query}
        result = await self._get_result(data)
        executions = result['data']['forcesExecutions']['executions']
        assert 'errors' not in result
        assert executions[0]['date'] == '2020-02-19T19:31:18+00:00'
        assert executions[0]['exitCode'] == '1'
        assert executions[0]['gitBranch'] == 'master'
        assert executions[0]['gitCommit'] == '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6'
        assert executions[0]['gitOrigin'] == 'http://test.com'
        assert executions[0]['gitRepo'] == 'Repository'
        assert executions[0]['kind'] == 'dynamic'
        assert len(executions[0]['log']) > 100
        assert isinstance(executions[0]['log'], str)
        assert executions[0]['strictness'] == 'strict'
        assert executions[0]['vulnerabilities'] == {
            "exploits": [
                {
                    "kind": "DAST",
                    "who": "https://test.com/test",
                    "where": "HTTP/Implementation"
                }
            ],
            "mockedExploits": [
                {
                    "kind": "DAST",
                    "who": "https://test.com/test",
                    "where": "HTTP/Implementation"
                }
            ],
            "acceptedExploits": [
                {
                    "kind": "DAST",
                    "who": "https://test.com/test/looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong",
                    "where": "HTTP/Implementatioooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooon"
                }
            ],
            "numOfVulnerabilitiesInExploits": 1,
            "numOfVulnerabilitiesInMockedExploits": 1,
            "numOfVulnerabilitiesInAcceptedExploits": 1
        }
        assert executions[1]['date'] == '2020-02-19T19:04:33+00:00'
        assert executions[1]['exitCode'] == '0'
        assert executions[1]['gitBranch'] == 'awesomeFeature'
        assert executions[1]['gitCommit'] == '23c3c76e7fe3bf9f2838f66e7b34c1358db2ff41'
        assert executions[1]['gitOrigin'] == 'https://test.com/test'
        assert executions[1]['gitRepo'] == 'Repository'
        assert executions[1]['kind'] == 'static'
        assert len(executions[1]['log']) > 100
        assert isinstance(executions[1]['log'], str)
        assert executions[1]['strictness'] == 'strict'
        assert executions[1]['vulnerabilities'] == {
            "exploits": [],
            "mockedExploits": [],
            "acceptedExploits": [
                {
                    "kind": "SAST",
                    "who": "Repository/folder/folder/file.cs",
                    "where": "55"
                },
                {
                    "kind": "SAST",
                    "who": "Repository/folder/folder/file2.cs",
                    "where": "3"
                },
                {
                    "kind": "SAST",
                    "who": "Repository/folder/folder/file3.cs",
                    "where": "8"
                },
                {
                    "kind": "SAST",
                    "who": "Repository/folder/folder/file3.cs",
                    "where": "9"
                },
                {
                    "kind": "SAST",
                    "who": "Repository/folder/folder/file4.cs",
                    "where": "10"
                }
            ],
            "numOfVulnerabilitiesInExploits": 0,
            "numOfVulnerabilitiesInMockedExploits": 0,
            "numOfVulnerabilitiesInAcceptedExploits": 5
        }
