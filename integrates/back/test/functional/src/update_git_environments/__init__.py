# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from json import (
    dumps,
)
from typing import (
    Any,
)


async def get_result_add(
    *,
    user: str,
    group: str,
    env_urls: list[str],
    root_id: str,
) -> dict[str, Any]:
    query: str = f"""
      mutation {{
        updateGitEnvironments(
            groupName: "{group}"
            id: "{root_id}"
            environmentUrls: {dumps(env_urls)}
        ) {{
            success
        }}
      }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_remove(
    *,
    user: str,
    group: str,
    env_urls: list[str],
    other: str,
    reason: str,
    root_id: str,
) -> dict[str, Any]:
    query: str = f"""
      mutation {{
        updateGitEnvironments(
            groupName: "{group}"
            id: "{root_id}"
            environmentUrls: {dumps(env_urls)}
            reason: {reason}
            other: "{other}"
        ) {{
            success
        }}
      }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutation_add(
    *,
    user: str,
    group_name: str,
    url: str,
    root_id: str,
    url_type: str,
) -> dict[str, Any]:
    query: str = """
        mutation AddGitEnvironmentUrl(
            $groupName: String!
            $rootId: ID!
            $url: String!
            $urlType: GitEnvironmentCloud!
        ) {
            addGitEnvironmentUrl(
                groupName: $groupName
                rootId: $rootId
                url: $url
                urlType: $urlType
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
            "url": url,
            "urlType": url_type,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutation_add_secret(
    *,
    user: str,
    group_name: str,
    key: str,
    url_id: str,
    value: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            addGitEnvironmentSecret(
                groupName: "{group_name}"
                urlId: "{url_id}"
                key: "{key}"
                value: "{value}"
                description: "user access for prod"
            ) {{
                success
            }}
        }}
    """

    data: dict[str, Any] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutation_remove(
    *,
    user: str,
    group_name: str,
    root_id: str,
    url_id: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            removeEnvironmentUrl(
                groupName: "{group_name}",
                urlId: "{url_id}"
                rootId: "{root_id}"
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutation_remove_secret(
    *,
    user: str,
    group_name: str,
    key: str,
    url_id: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            removeEnvironmentUrlSecret(
                key: "{key}"
                groupName: "{group_name}"
                urlId: "{url_id}"
            ) {{
                success
            }}
        }}
    """

    data: dict[str, Any] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
