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
) -> Dict[str, Any]:
    query: str = f"""
      mutation {{
        addGitRoot(
          branch: "trunk"
          credentials: {{
            token: "token"
            name: "Credentials test"
            type: HTTPS
          }}
          environment: "production"
          gitignore: []
          groupName: "{group}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/universe"
        ) {{
          rootId
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
