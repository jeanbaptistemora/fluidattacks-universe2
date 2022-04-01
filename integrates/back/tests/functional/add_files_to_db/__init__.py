# pylint: disable=import-error
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
)


async def get_result(
    *,
    description: str,
    file_name: str,
    group_name: str,
    user_email: str,
) -> dict[str, Any]:
    path: str = os.path.dirname(os.path.abspath(__file__))
    file_path: str = f"{path}/{file_name}"
    result: dict[str, Any] = {}
    with open(file_path, "rb"):
        file_data: list[dict[str, str]] = [
            {
                "description": description,
                "fileName": file_name,
                "uploadDate": "",
            }
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
        variables: dict[str, Any] = {
            "filesData": json.dumps(file_data),
            "groupName": group_name,
        }
        data: dict[str, Any] = {"query": query, "variables": variables}
        result = await get_graphql_result(
            data,
            stakeholder=user_email,
            context=get_new_context(),
        )
    return result
