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
)


async def get_result(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    firts = 50

    query: str = f"""query {{
    group(groupName: "{group}") {{
      executionsConnections(after: "", first: {firts}, search: "") {{
        edges {{
          node {{
            groupName
            gracePeriod
            date
            exitCode
            gitBranch
            gitCommit
            gitOrigin
            gitRepo
            executionId
            kind
            severityThreshold
            strictness
            vulnerabilities {{
              numOfAcceptedVulnerabilities
              numOfOpenVulnerabilities
              numOfClosedVulnerabilities
            }}
          }}
        }}
        pageInfo {{
          endCursor
          hasNextPage
        }}
      }}
      name
    }}
  }}"""

    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
