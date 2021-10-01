from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import json
import os
from typing import (
    Any,
    Dict,
    List,
)


async def get_result(
    *,
    user: str,
    group: str,
) -> Dict[str, Any]:
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = "test-anim.gif"
    file_path: str = f"{path}/{filename}"
    result: Dict[str, Any] = {}
    with open(file_path, "rb"):
        file_data: List[Dict[str, str]] = [
            {"description": "test", "fileName": filename, "uploadDate": ""}
        ]
        query: str = """
            mutation AddFilesToDb(
                $filesData: JSONString!, $groupName: String!
            ) {
                addFilesToDb (
                    filesData: $filesData,
                    groupName: $groupName) {
                        success
                }
            }
        """
        variables: Dict[str, Any] = {
            "filesData": json.dumps(file_data),
            "groupName": group,
        }
        data: Dict[str, Any] = {"query": query, "variables": variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
