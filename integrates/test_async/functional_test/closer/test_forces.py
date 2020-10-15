import pytest

from test_async.functional_test.closer.utils import get_result

pytestmark = pytest.mark.asyncio


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

    query = f"""
        query {{
            forcesExecutions(
                projectName: "{group_name}",
                fromDate: "2020-02-01T00:00:00Z",
                toDate: "2020-02-28T23:59:59Z"
            ) {{
                fromDate
                projectName
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
                        acceptedExploits {{
                            exploitability
                            kind
                            state
                            who
                            where
                        }}
                        exploits {{
                            exploitability
                            kind
                            state
                            who
                            where
                        }}
                        integratesExploits {{
                            exploitability
                            kind
                            state
                            who
                            where
                        }}
                        numOfVulnerabilitiesInAcceptedExploits
                        numOfVulnerabilitiesInExploits
                        numOfVulnerabilitiesInIntegratesExploits
                    }}
                }}
                __typename
            }}
        }}
    """
    data = {'query': query}
    result = await get_result(data)
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
                "exploitability": None,
                "kind": "DAST",
                "state": None,
                "who": "https://test.com/test",
                "where": "HTTP/Implementation"
            }
        ],
        "integratesExploits": [
            {
                "exploitability": None,
                "kind": "DAST",
                "state": None,
                "who": "https://test.com/test",
                "where": "HTTP/Implementation"
            }
        ],
        "acceptedExploits": [
            {
                "exploitability": None,
                "kind": "DAST",
                "state": None,
                "who": "https://test.com/test/looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong",
                "where": "HTTP/Implementatioooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooon"
            }
        ],
        "numOfVulnerabilitiesInExploits": 1,
        "numOfVulnerabilitiesInIntegratesExploits": 1,
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
        "integratesExploits": [],
        "acceptedExploits": [
            {
                "exploitability": None,
                "kind": "SAST",
                "state": None,
                "who": "Repository/folder/folder/file.cs",
                "where": "55"
            },
            {
                "exploitability": None,
                "kind": "SAST",
                "state": None,
                "who": "Repository/folder/folder/file2.cs",
                "where": "3"
            },
            {
                "exploitability": None,
                "kind": "SAST",
                "state": None,
                "who": "Repository/folder/folder/file3.cs",
                "where": "8"
            },
            {
                "exploitability": None,
                "kind": "SAST",
                "state": None,
                "who": "Repository/folder/folder/file3.cs",
                "where": "9"
            },
            {
                "exploitability": None,
                "kind": "SAST",
                "state": None,
                "who": "Repository/folder/folder/file4.cs",
                "where": "10"
            }
        ],
        "numOfVulnerabilitiesInExploits": 0,
        "numOfVulnerabilitiesInIntegratesExploits": 0,
        "numOfVulnerabilitiesInAcceptedExploits": 5
    }

    query = f"""
        query {{
            forcesExecutionsNew(
                projectName: "{group_name}",
                fromDate: "2020-02-01T00:00:00Z",
                toDate: "2020-02-28T23:59:59Z"
            ) {{
                fromDate
                toDate
                executions{{
                    projectName
                }}

                __typename
            }}
        }}
    """
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['forcesExecutionsNew']['fromDate'] == '2020-02-01 00:00:00+00:00'
    assert result['data']['forcesExecutionsNew']['toDate'] == '2020-02-28 23:59:59+00:00'
    assert result['data']['forcesExecutionsNew']['executions'] == []

    execution_id = '08c1e735a73243f2ab1ee0757041f80e'
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
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['forcesExecution']['projectName'] == group_name
    assert result['data']['forcesExecution']['execution_id'] == execution_id
    assert result['data']['forcesExecution']['exitCode'] == '0'
    assert result['data']['forcesExecution']['gitBranch'] == 'unable to retrieve'
    assert result['data']['forcesExecution']['gitCommit'] == 'unable to retrieve'
    assert result['data']['forcesExecution']['gitOrigin'] == 'unable to retrieve'
    assert result['data']['forcesExecution']['gitRepo'] == 'unable to retrieve'
    assert result['data']['forcesExecution']['kind'] == 'other'
    assert result['data']['forcesExecution']['strictness'] == 'lax'
    assert result['data']['forcesExecution']['vulnerabilities']['numOfAcceptedVulnerabilities'] == 0
    assert result['data']['forcesExecution']['vulnerabilities']['numOfClosedVulnerabilities'] == 8
    assert result['data']['forcesExecution']['vulnerabilities']['numOfOpenVulnerabilities'] == 32
    assert result['data']['forcesExecution']['vulnerabilities']['accepted'] == []
    assert len(result['data']['forcesExecution']['vulnerabilities']['closed']) == 8
    assert len(result['data']['forcesExecution']['vulnerabilities']['open']) == 32
