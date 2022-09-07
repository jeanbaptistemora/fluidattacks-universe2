# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    nickname: str,
    url: str,
) -> Dict[str, Any]:
    mutation: str = f"""
      mutation {{
        addUrlRoot(
          groupName: "{group}"
          nickname: "{nickname}"
          url: "{url}"
        ) {{
          rootId
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
