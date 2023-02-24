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


async def get_result(
    *,
    user: str,
    group: str,
    key: str,
    branch: str,
    url: str,
) -> dict[str, Any]:
    query: str = f"""
      mutation {{
        validateGitAccess(
            branch: "{branch}"
            credentials: {{
                key: "{key}"
                name: "SSH Key"
                type: SSH
            }}
            groupName: "{group}"
            url: "{url}"
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
