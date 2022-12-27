# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    group: str,
    root_id: str,
) -> Dict[str, Any]:
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
    data: Dict[str, str] = {
        "query": mutation,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
