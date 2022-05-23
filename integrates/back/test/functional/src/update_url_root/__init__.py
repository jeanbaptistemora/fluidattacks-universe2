# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def put_mutation(
    *,
    group_name: str,
    root_id: str,
    nickname: str,
    user: str,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateURLRoot (
            $groupName: String!
            $rootId: ID!
            $nickname: String!
        ) {
        updateUrlRoot(
            groupName: $groupName
            rootId: $rootId
            nickname: $nickname
        ) {
            success
        }
      }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "rootId": root_id,
            "nickname": nickname,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_query(
    *,
    group_name: str,
    root_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = """
        query GetRoots($rootId: ID!, $groupName: String!) {
            root(groupName: $groupName, rootId: $rootId) {
                ... on URLRoot {
                    __typename
                    host
                    id
                    nickname
                    path
                    state
                }
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "rootId": root_id,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
