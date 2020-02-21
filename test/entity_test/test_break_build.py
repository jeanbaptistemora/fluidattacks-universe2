import os
from collections import OrderedDict

import pytest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from graphene.test import Client
from jose import jwt

from backend.api.schema import SCHEMA


class BreakBuildExecutionsTests(TestCase):

    def _get_result(self, query, testing_client):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'integratesuser@gmail.com',
                'user_role': 'customer',
                'company': 'unittest',
                'first_name': 'unit',
                'last_name': 'test'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        if testing_client:

            return testing_client.execute(query, context=request)

        return SCHEMA.execute(query, context=request)

    def test_project_name(self):
        valid_project_name = 'unittesting'
        query = f'''
          query {{
            breakBuildExecutions(
                projectName: "{valid_project_name}",
            ) {{
              projectName
            }}
          }}
        '''
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client)
        assert not result.get('errors')
        assert result['data']['breakBuildExecutions']['projectName'] \
            == valid_project_name

    def test_executions(self):
        project_name = 'unittesting'
        query = """
          query {
            breakBuildExecutions(
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
        testing_client = Client(SCHEMA)
        result = self._get_result(query, testing_client)
        executions = result['data']['breakBuildExecutions']['executions']

        assert not result.get('errors')

        assert executions[0]['projectName'] == project_name
        assert executions[0]['identifier'] == '33e5d863252940edbfb144ede56d56cf'
        assert executions[0]['date'] == '2020-02-19T19:31:18+00:00'
        assert executions[0]['exitCode'] == '0'
        assert executions[0]['gitBranch'] == 'master'
        assert executions[0]['gitCommit'] == '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6'
        assert executions[0]['gitOrigin'] == 'http://test.com'
        assert executions[0]['gitRepo'] == 'Repository'
        assert executions[0]['kind'] == 'dynamic'
        assert len(executions[0]['log']) > 100
        assert isinstance(executions[0]['log'], str)
        assert executions[0]['strictness'] == 'strict'
        assert executions[0]['vulnerabilities'] == {
            "exploits": [],
            "mockedExploits": [],
            "acceptedExploits": [
                {
                    "kind": "DAST",
                    "who": "https://test.com/test",
                    "where": "HTTP/Implementation"
                },
                {
                    "kind": "DAST",
                    "who": "https://test.com/test",
                    "where": "HTTP/Implementation"
                }
            ],
            "numOfVulnerabilitiesInExploits": 0,
            "numOfVulnerabilitiesInMockedExploits": 0,
            "numOfVulnerabilitiesInAcceptedExploits": 2
        }

        assert executions[1]['projectName'] == project_name
        assert executions[1]['identifier'] == 'a125217504d447ada2b81da3e4bdab0e'
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
