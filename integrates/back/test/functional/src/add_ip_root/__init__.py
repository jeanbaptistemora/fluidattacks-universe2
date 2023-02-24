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
    nickname: str,
    address: str,
) -> dict[str, Any]:
    mutation: str = f"""
      mutation {{
        addIpRoot(
          groupName: "{group}"
          nickname: "{nickname}"
          address: "{address}"
        ) {{
          rootId
          success
        }}
      }}
    """
    data: dict[str, str] = {
        "query": mutation,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
