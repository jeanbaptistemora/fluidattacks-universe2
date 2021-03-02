import os
import pytest
import textwrap

from starlette.datastructures import UploadFile

from back.tests.functional.service_forces.utils import get_result


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('old')
async def test_forces():
    group_name = 'unittesting'
    query = f"""
        mutation {{
            updateForcesAccessToken(projectName: "{group_name}"){{
                success
                sessionJwt
            }}
        }}
    """
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' in result
    assert result['errors'][0]['message'] == 'Access denied'

    execution_id = '18c1e735a73243f2ab1ee0757041f80e'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../unit/mock/test-log.log')
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, 'text/plain')
        query = '''
            mutation AddForcesExecutionMutation(
                $file: Upload!,
                $date: DateTime!,
                $groupName: String!,
                $executionId: String!
            ) {
                addForcesExecution (
                    projectName: $groupName,
                    execution_id: $executionId,
                    date: $date,
                    exitCode: "1",
                    gitBranch: "master",
                    gitCommit: "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
                    gitOrigin: "http://origin-test.com",
                    gitRepo: "Repository",
                    kind: "dynamic",
                    log: $file,
                    strictness: "strict",
                    vulnerabilities: {
                        accepted: [
                            {
                                exploitability: 3.1
                                kind: "DAST"
                                state: ACCEPTED
                                where: "HTTP/Implementation"
                                who: "https://accepted.com/test"
                            }
                        ]
                        closed: [
                            {
                                exploitability: 3.2
                                kind: "DAST"
                                state: CLOSED
                                where: "HTTP/Implementation"
                                who: "https://closed.com/test"
                            }
                        ]
                        open: [
                            {
                                exploitability: 3.3
                                kind: "DAST"
                                state: OPEN
                                where: "HTTP/Implementation"
                                who: "https://open.com/test"
                            }
                        ]
                    }
                ){
                    success
                }
            }
        '''
        variables = {
            'file': uploaded_file,
            'date': '2020-02-20T00:00:00Z',
            'groupName': group_name,
            'executionId': execution_id,
        }
        data = {'query': query, 'variables': variables}
        result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['addForcesExecution']['success']

    query = f"""
        query {{
            forcesExecutions(
                projectName: "{group_name}",
                fromDate: "2020-02-01T00:00:00Z",
                toDate: "2020-02-28T23:59:59Z"
            ) {{
                fromDate
                toDate
                executions {{
                    projectName
                    execution_id
                    date
                    exitCode
                    gitBranch
                    gitCommit
                    gitOrigin
                    gitRepo
                    kind
                    log
                    strictness
                    vulnerabilities {{
                        accepted {{
                            exploitability
                            kind
                            state
                            where
                            who
                        }}

                        closed {{
                            exploitability
                            kind
                            state
                            where
                            who
                        }}
                        numOfAcceptedVulnerabilities
                        numOfClosedVulnerabilities
                        numOfOpenVulnerabilities
                        open {{
                            exploitability
                            kind
                            state
                            where
                            who
                        }}
                    }}
                }}

                __typename
            }}
        }}
    """
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert result['data']['forcesExecutions']['fromDate'] == '2020-02-01 00:00:00+00:00'
    assert result['data']['forcesExecutions']['toDate'] == '2020-02-28 23:59:59+00:00'
    executions = result['data']['forcesExecutions']['executions']
    execution = [execution for execution in executions if execution['execution_id'] == execution_id][0]
    assert execution['projectName'] == group_name
    assert execution['date'] == '2020-02-20T00:00:00+00:00'
    assert execution['exitCode'] == '1'
    assert execution['gitBranch'] == 'master'
    assert execution['gitCommit'] == '2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2'
    assert execution['gitOrigin'] == 'http://origin-test.com'
    assert execution['gitRepo'] == 'Repository'
    assert execution['kind'] == 'dynamic'
    assert execution['log'] == textwrap.dedent(
        '''\
        .LOG

        10:39 AM 10/17/2020
        tes1
        10:40 AM 10/17/2020
        test2
        10:40 AM 10/17/2020
        test3
        10:40 AM 10/17/2020
        tes4
        10:41 AM 10/17/2020
        test5'''
    )
    assert execution['strictness'] == 'strict'
    assert execution['vulnerabilities']['accepted'] == [
        {
            'exploitability': '3.1',
            'kind': 'DAST',
            'state': 'ACCEPTED',\
            'where': 'HTTP/Implementation',
            'who': 'https://accepted.com/test'
        }
    ]
    assert execution['vulnerabilities']['closed'] == [
        {
            'exploitability': '3.2',
            'kind': 'DAST',
            'state': 'CLOSED',
            'where': 'HTTP/Implementation',
            'who': 'https://closed.com/test'
        }
    ]
    assert execution['vulnerabilities']['numOfAcceptedVulnerabilities'] == 1
    assert execution['vulnerabilities']['numOfClosedVulnerabilities'] == 1
    assert execution['vulnerabilities']['numOfOpenVulnerabilities'] == 1
    assert execution['vulnerabilities']['open'] == [
        {
            'exploitability': '3.3',
            'kind': 'DAST',
            'state': 'OPEN',
            'where': 'HTTP/Implementation',
            'who': 'https://open.com/test'
        }
    ]

    query = f"""
        query {{
            forcesExecution(
                projectName: "{group_name}",
                executionId: "{execution_id}"
            ) {{
                projectName
                execution_id
                date
                exitCode
                gitBranch
                gitCommit
                gitOrigin
                gitRepo
                kind
                log
                strictness
                vulnerabilities {{
                    accepted {{
                        exploitability
                        kind
                        state
                        who
                        where
                    }}
                    closed {{
                        exploitability
                        kind
                        state
                        who
                        where
                    }}
                    numOfAcceptedVulnerabilities
                    numOfClosedVulnerabilities
                    numOfOpenVulnerabilities
                    open {{
                        exploitability
                        kind
                        state
                        who
                        where
                    }}
                }}
            }}
        }}
    """
    data = {'query': query}
    result = await get_result(data, stakeholder='integratesmanager@gmail.com')
    assert 'errors' not in result
    assert result['data']['forcesExecution']['projectName'] == group_name
    assert result['data']['forcesExecution']['date'] == '2020-02-20T00:00:00+00:00'
    assert result['data']['forcesExecution']['exitCode'] == '1'
    assert result['data']['forcesExecution']['gitBranch'] == 'master'
    assert result['data']['forcesExecution']['gitCommit'] == '2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2'
    assert result['data']['forcesExecution']['gitOrigin'] == 'http://origin-test.com'
    assert result['data']['forcesExecution']['gitRepo'] == 'Repository'
    assert result['data']['forcesExecution']['kind'] == 'dynamic'
    assert result['data']['forcesExecution']['log'] == textwrap.dedent(
        '''\
        .LOG

        10:39 AM 10/17/2020
        tes1
        10:40 AM 10/17/2020
        test2
        10:40 AM 10/17/2020
        test3
        10:40 AM 10/17/2020
        tes4
        10:41 AM 10/17/2020
        test5'''
    )
    assert result['data']['forcesExecution']['strictness'] == 'strict'
    assert result['data']['forcesExecution']['vulnerabilities']['accepted'] == [
        {
            'exploitability': '3.1',
            'kind': 'DAST',
            'state': 'ACCEPTED',\
            'where': 'HTTP/Implementation',
            'who': 'https://accepted.com/test'
        }
    ]
    assert result['data']['forcesExecution']['vulnerabilities']['closed'] == [
        {
            'exploitability': '3.2',
            'kind': 'DAST',
            'state': 'CLOSED',
            'where': 'HTTP/Implementation',
            'who': 'https://closed.com/test'
        }
    ]
    assert result['data']['forcesExecution']['vulnerabilities']['numOfAcceptedVulnerabilities'] == 1
    assert result['data']['forcesExecution']['vulnerabilities']['numOfClosedVulnerabilities'] == 1
    assert result['data']['forcesExecution']['vulnerabilities']['numOfOpenVulnerabilities'] == 1
    assert result['data']['forcesExecution']['vulnerabilities']['open'] == [
        {
            'exploitability': '3.3',
            'kind': 'DAST',
            'state': 'OPEN',
            'where': 'HTTP/Implementation',
            'who': 'https://open.com/test'
        }
    ]
