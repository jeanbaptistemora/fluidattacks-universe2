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
    root_id: str,
) -> dict[str, Any]:
    mutation: str = f"""
      mutation {{
        updateRootCloningStatus(
          groupName: "{group}"
          id: "{root_id}"
          status: OK
          message: "root update test"
        ) {{
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
