from back.tests.functional.reviewer.utils import (
    get_result,
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
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_resource() -> None:
    group_name = "unittesting"
    file_name = "test.zip"
    query = f"""{{
        resources(groupName: "{group_name}"){{
            groupName
            files
            __typename
        }}
    }}"""
    data: Dict[str, Any] = {"query": query}
    result = await get_result(data)
    assert result["data"]["resources"]["groupName"] == "unittesting"
    assert file_name in result["data"]["resources"]["files"]
    assert "shell.exe" in result["data"]["resources"]["files"]
    assert "shell2.exe" in result["data"]["resources"]["files"]
    assert "asdasd.py" in result["data"]["resources"]["files"]
    files = json.loads(result["data"]["resources"]["files"])

    query = f"""
        mutation {{
            downloadFile (
                filesData: \"\\\"{file_name}\\\"\",
                groupName: "{group_name}"
            ) {{
                success
                url
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["downloadFile"]
    assert result["data"]["downloadFile"]["success"]
    assert "url" in result["data"]["downloadFile"]

    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../../unit/mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "image/gif")
        files_data = [
            {
                "description": "test",
                "fileName": test_file.name.split("/")[2],
                "uploadDate": "",
            }
        ]
        query = """
            mutation UploadFileMutation(
                $file: Upload!, $filesData: JSONString!, $groupName: String!
            ) {
                addFiles (
                    file: $file,
                    filesData: $filesData,
                    groupName: $groupName) {
                        success
                }
            }
        """
        variables = {
            "file": uploaded_file,
            "filesData": json.dumps(files_data),
            "groupName": group_name,
        }
    data = {"query": query, "variables": variables}
    result = await get_result(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

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
    file_data = {"description": "", "fileName": "", "uploadDate": ""}
    variables = {"filesData": json.dumps(file_data), "groupName": group_name}
    data = {"query": query, "variables": variables}
    result = await get_result(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    query = f"""{{
        resources(groupName: "{group_name}"){{
            groupName
            files
            __typename
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data)
    assert json.loads(result["data"]["resources"]["files"]) == files
