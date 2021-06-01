from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
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
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
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
    """Check for project resources"""
    query = """{
      resources(projectName: "unittesting"){
        projectName
        files
        __typename
      }
    }"""
    data = {"query": query}
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "resources" in result["data"]
    assert result["data"]["resources"]["projectName"] == "unittesting"
    assert "test.zip" in result["data"]["resources"]["files"]
    assert "shell.exe" in result["data"]["resources"]["files"]
    assert "shell2.exe" in result["data"]["resources"]["files"]
    assert "asdasd.py" in result["data"]["resources"]["files"]


@pytest.mark.changes_db
async def test_add_files() -> None:
    """Check for addFiles mutation."""
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "image/gif")
        file_data = [
            {
                "description": "test",
                "fileName": test_file.name.split("/")[2],
                "uploadDate": "",
            }
        ]
        query = """
            mutation UploadFileMutation(
                $file: Upload!, $filesData: JSONString!, $projectName: String!
            ) {
                addFiles (
                    file: $file,
                    filesData: $filesData,
                    projectName: $projectName) {
                        success
                }
            }
        """
        variables = {
            "file": uploaded_file,
            "filesData": json.dumps(file_data),
            "projectName": "UNITTESTING",
        }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    if "errors" not in result:
        assert "errors" not in result
        assert "success" in result["data"]["addFiles"]
        assert result["data"]["addFiles"]["success"]
    else:
        pytest.skip("Expected error")


@pytest.mark.changes_db
async def test_download_file() -> None:
    """Check for downloadFile mutation."""
    query = """
        mutation {
          downloadFile (
            filesData: \"\\\"unittesting-422286126.yaml\\\"\",
            projectName: "unittesting") {
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
        mutation RemoveFileMutation($filesData: JSONString!, $projectName: String!) {
            removeFiles(filesData: $filesData, projectName: $projectName) {
            success
            }
        }
    """
    variables = {
        "filesData": json.dumps(file_data),
        "projectName": "UNITTESTING",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["removeFiles"]
    assert result["data"]["removeFiles"]["success"]
