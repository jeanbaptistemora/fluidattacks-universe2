# pylint: disable=import-error
from back.test.functional.src.utils import (
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
)


async def get_result(
    *,
    user: str,
    finding: str,
    yaml_file_name: str,
) -> dict[str, Any]:
    query: str = """
            mutation UploadFileMutation(
                $file: Upload!, $findingId: String!
            ) {
                uploadFile (
                    file: $file,
                    findingId: $findingId
                ) {
                    success
                }
            }
        """
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = f"{path}/{yaml_file_name}"
    with open(filename, "rb") as test_file:
        uploaded_file: UploadFile = UploadFile(
            test_file.name, test_file, "text/x-yaml"
        )
        variables: dict[str, Any] = {
            "file": uploaded_file,
            "findingId": finding,
        }
        data: dict[str, Any] = {"query": query, "variables": variables}
        result: dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result


async def update_services(
    *,
    user: str,
    group: str,
    has_machine: str,
    has_squad: str,
    subscription: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroup(
                comments: "",
                groupName: "{group}",
                subscription: {subscription},
                hasSquad: {has_squad},
                hasAsm: true,
                hasMachine: {has_machine},
                reason: NONE,
                tier: OTHER,
                service: WHITE,
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_group_vulnerabilities(
    *,
    user: str,
    group_name: str,
    state_status: str | None = None,
    treatment_status: str | None = None,
) -> dict:
    query: str = """
        query GetGroupVulnerabilities(
            $after: String
            $first: Int
            $groupName: String!
            $stateStatus: String
            $treatment: String
        ) {
            group(groupName: $groupName) {
                name
                vulnerabilities(
                    stateStatus: $stateStatus,
                    treatment: $treatment,
                    after: $after,
                    first: $first
                ) {
                    edges {
                        node {
                            currentState
                            state
                            treatment
                            treatmentStatus
                            where
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
    """

    data: dict = {
        "query": query,
        "variables": {
            "first": 100,
            "groupName": group_name,
            "stateStatus": state_status,
            "treatment": treatment_status,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
