import os
import pytest
import textwrap

from starlette.datastructures import UploadFile

from test_async.functional_test.service_forces.utils import get_result

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

    execution_id = '18c1e735a73243f2ab1ee0757041f80e'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../../mock/test-log.log')
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
