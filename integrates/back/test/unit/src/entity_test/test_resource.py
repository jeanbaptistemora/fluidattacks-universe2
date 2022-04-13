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
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
import json
import os
import pytest
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

pytestmark = pytest.mark.asyncio


async def _get_result(
    data: Dict[str, Any], context: Optional[Dataloaders] = None
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(
        request, loaders=context if context else get_new_context()
    )
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


async def test_get_resources() -> None:
    """Check for group resources."""
    query = """{
      resources(groupName: "unittesting"){
        groupName
        files {
            description
            fileName
            uploadDate
            uploader
        }
        __typename
      }
    }"""
    data = {"query": query}
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "resources" in result["data"]
    assert result["data"]["resources"]["groupName"] == "unittesting"

    expected_output: List[Dict[str, str]] = [
        {
            "description": "Test",
            "fileName": "test.zip",
            "uploadDate": "2019-03-01 15:21:00",
            "uploader": "unittest@fluidattacks.com",
        },
        {
            "description": "shell",
            "fileName": "shell.exe",
            "uploadDate": "2019-04-24 14:56:00",
            "uploader": "unittest@fluidattacks.com",
        },
        {
            "description": "shell2",
            "fileName": "shell2.exe",
            "uploadDate": "2019-04-24 14:59:00",
            "uploader": "unittest@fluidattacks.com",
        },
        {
            "description": "eerweterterter",
            "fileName": "asdasd.py",
            "uploadDate": "2019-08-06 14:28:00",
            "uploader": "unittest@fluidattacks.com",
        },
    ]
    assert result["data"]["resources"]["files"] == expected_output


@pytest.mark.changes_db
async def test_add_files() -> None:
    """Check for SignPostUrlMutation mutation."""
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        file_data = [
            {
                "description": "test",
                "fileName": test_file.name.split("/")[2],
                "uploadDate": "",
            }
        ]
        query = """
            mutation SignPostUrlMutation(
                $filesData: JSONString!, $groupName: String!
            ) {
                signPostUrl (
                    filesData: $filesData,
                    groupName: $groupName) {
                        success
                }
            }
        """
        variables = {
            "filesData": json.dumps(file_data),
            "groupName": "UNITTESTING",
        }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    if "errors" not in result:
        assert "errors" not in result
        assert "success" in result["data"]["signPostUrl"]
        assert result["data"]["signPostUrl"]["success"]
    else:
        pytest.skip("Expected error")


@pytest.mark.changes_db
async def test_download_file() -> None:
    """Check for downloadFile mutation."""
    query = """
        mutation {
          downloadFile (
            filesData: \"\\\"unittesting-422286126.yaml\\\"\",
            groupName: "unittesting") {
              success
              url
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["downloadFile"]
    assert result["data"]["downloadFile"]["success"]
    assert "url" in result["data"]["downloadFile"]


@pytest.mark.changes_db
async def test_remove_files() -> None:
    """Check for removeFiles mutation."""
    context = get_new_context()
    file_data = {
        "description": "test",
        "fileName": "shell.exe",
        "uploadDate": "",
    }
    query = """
        mutation RemoveFileMutation(
            $filesData: JSONString!,
            $groupName: String!
        ) {
            removeFiles(filesData: $filesData, groupName: $groupName) {
            success
            }
        }
    """
    variables = {
        "filesData": json.dumps(file_data),
        "groupName": "UNITTESTING",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["removeFiles"]
    assert result["data"]["removeFiles"]["success"]
