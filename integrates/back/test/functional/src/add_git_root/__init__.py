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


async def get_result(
    *,
    user: str,
    group: str,
    credentials: dict,
) -> dict:
    query: str = """
      mutation AddGitRoot (
        $groupName: String!, $credentials: RootCredentialsInput
      ) {
        addGitRoot(
          branch: "trunk"
          credentials: $credentials
          environment: "production"
          gitignore: []
          groupName: $groupName
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/universe"
        ) {
          rootId
          success
        }
      }
    """
    data: dict = {
        "query": query,
        "variables": {
            "groupName": group,
            "credentials": credentials,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
