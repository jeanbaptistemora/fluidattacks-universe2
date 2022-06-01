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
    Dict,
)


async def get_result_add(
    *,
    user: str,
    group: str,
    env_urls: list[str],
    root_id: str,
) -> Dict[str, Any]:
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
    data: Dict[str, str] = {
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
) -> Dict[str, Any]:
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
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
