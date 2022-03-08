# pylint: disable=import-error
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import json
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    query: str = """
        mutation RemoveFileMutation(
            $filesData: JSONString!,
            $groupName: String!
        ) {
            removeFiles(filesData: $filesData, groupName: $groupName) {
                success
            }
        }
    """
    file_data: Dict[str, str] = {
        "description": "Test",
        "fileName": "test.zip",
        "uploadDate": "2019-03-01 15:21",
    }
    variables: Dict[str, Any] = {
        "filesData": json.dumps(file_data),
        "groupName": group,
    }
    data: Dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
