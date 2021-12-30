from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import os
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    execution: str = "18c1e735a73243f2ab1ee0757041f80e"
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = os.path.join(path, "../../unit/mock/test-log.log")
    result: Dict[str, Any] = {}
    with open(filename, "rb") as test_file:
        uploaded_file: UploadFile = UploadFile(
            test_file.name, test_file, "text/plain"
        )
        query: str = """
            mutation AddForcesExecutionMutation(
                $file: Upload!,
                $date: DateTime!,
                $groupName: String!,
                $executionId: String!
            ) {
                addForcesExecution (
                    groupName: $groupName,
                    executionId: $executionId,
                    date: $date,
                    exitCode: "1",
                    gitBranch: "master",
                    gitCommit: "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
                    gitOrigin: "http://origin-test.com",
                    gitRepo: "Repository",
                    kind: "dynamic",
                    log: $file,
                    strictness: "strict",
                    gracePeriod: 0
                    severityThreshold: 0.0
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
        """
        variables: Dict[str, Any] = {
            "file": uploaded_file,
            "date": "2020-02-20T00:00:00Z",
            "groupName": group,
            "executionId": execution,
        }
        data: Dict[str, Any] = {"query": query, "variables": variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
