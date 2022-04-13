# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
    create_dummy_session,
)
import pytest
from typing import (
    Any,
    Dict,
)

pytestmark = pytest.mark.asyncio


async def _get_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username="integratesuser@gmail.com")
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


async def test_group_name() -> None:
    """Check for group_name field."""
    query = """{
      forcesExecutions(groupName: "unittesting"){
        groupName
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["forcesExecutions"]["groupName"] == "unittesting"


async def _test_executions() -> None:
    """Check for executions field."""
    query = """
      query {
        forcesExecutions(
            groupName: "unittesting",
            fromDate: "2020-02-01T00:00:00Z",
            toDate: "2020-02-28T23:59:59Z"
        ) {
          __typename
          executions {
            groupName
            executionId
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
              integratesExploits {
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
              numOfVulnerabilitiesInIntegratesExploits
              numOfVulnerabilitiesInAcceptedExploits
            }
          }
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    executions = result["data"]["forcesExecutions"]["executions"]
    assert "errors" not in result
    assert executions[0]["date"] == "2020-02-19T19:31:18+00:00"
    assert executions[0]["exitCode"] == "1"
    assert executions[0]["gitBranch"] == "master"
    assert (
        executions[0]["gitCommit"]
        == "6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6"
    )
    # FP: local testing
    assert executions[0]["gitOrigin"] == "http://test.com"  # NOSONAR
    assert executions[0]["gitRepo"] == "Repository"
    assert executions[0]["kind"] == "dynamic"
    assert len(executions[0]["log"]) > 100
    assert isinstance(executions[0]["log"], str)
    assert executions[0]["strictness"] == "strict"
    assert executions[0]["vulnerabilities"] == {
        "exploits": [
            {
                "kind": "DAST",
                "who": "https://test.com/test",
                "where": "HTTP/Implementation",
            }
        ],
        "integratesExploits": [
            {
                "kind": "DAST",
                "who": "https://test.com/test",
                "where": "HTTP/Implementation",
            }
        ],
        "acceptedExploits": [
            {
                "kind": "DAST",
                "who": "https://test.com/test/looooooooooooooooooooooo"
                "oooooooooooooooooooooooooooooooooooooooooooooooooooong",
                "where": "HTTP/Implementatiooooooooooooooooooooooooooo"
                "ooooooooooooooooooooooooooooooooooooooooooooooooooooooon",
            }
        ],
        "numOfVulnerabilitiesInExploits": 1,
        "numOfVulnerabilitiesInIntegratesExploits": 1,
        "numOfVulnerabilitiesInAcceptedExploits": 1,
    }
    assert executions[1]["date"] == "2020-02-19T19:04:33+00:00"
    assert executions[1]["exitCode"] == "0"
    assert executions[1]["gitBranch"] == "awesomeFeature"
    assert (
        executions[1]["gitCommit"]
        == "23c3c76e7fe3bf9f2838f66e7b34c1358db2ff41"
    )
    assert executions[1]["gitOrigin"] == "https://test.com/test"
    assert executions[1]["gitRepo"] == "Repository"
    assert executions[1]["kind"] == "static"
    assert len(executions[1]["log"]) > 100
    assert isinstance(executions[1]["log"], str)
    assert executions[1]["strictness"] == "strict"
    assert executions[1]["vulnerabilities"] == {
        "exploits": [],
        "integratesExploits": [],
        "acceptedExploits": [
            {
                "kind": "SAST",
                "who": "Repository/folder/folder/file.cs",
                "where": "55",
            },
            {
                "kind": "SAST",
                "who": "Repository/folder/folder/file2.cs",
                "where": "3",
            },
            {
                "kind": "SAST",
                "who": "Repository/folder/folder/file3.cs",
                "where": "8",
            },
            {
                "kind": "SAST",
                "who": "Repository/folder/folder/file3.cs",
                "where": "9",
            },
            {
                "kind": "SAST",
                "who": "Repository/folder/folder/file4.cs",
                "where": "10",
            },
        ],
        "numOfVulnerabilitiesInExploits": 0,
        "numOfVulnerabilitiesInIntegratesExploits": 0,
        "numOfVulnerabilitiesInAcceptedExploits": 5,
    }
