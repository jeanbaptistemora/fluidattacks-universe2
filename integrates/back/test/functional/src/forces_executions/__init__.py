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


def get_query() -> str:
    return """
      query(
        $first: Int
        $fromDate: DateTime
        $gitRepo: String
        $groupName: String!
        $search: String
        $toDate: DateTime
        $type: String
      ) {
        group(groupName: $groupName) {
          executionsConnections(
            first: $first,
            fromDate: $fromDate,
            gitRepo: $gitRepo,
            search: $search,
            toDate: $toDate,
            type: $type
          ) {
            edges {
              node {
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
                vulnerabilities {
                  numOfAcceptedVulnerabilities
                  numOfOpenVulnerabilities
                  numOfClosedVulnerabilities
                }
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
          name
        }
      }
    """


async def get_result(
    *,
    user: str,
    from_date: str = "",
    group: str,
    repo: str = "",
    search: str = "",
    to_date: str = "",
    kind: str = "",
) -> dict[str, Any]:
    first = 50
    query: str = get_query()

    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "first": first,
            "fromDate": from_date,
            "gitRepo": repo,
            "groupName": group,
            "search": search,
            "toDate": to_date,
            "type": kind,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
