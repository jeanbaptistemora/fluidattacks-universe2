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


async def put_mutation(
    *,
    user: str,
    branch: str,
    environment: str,
    gitignore: str,
    group_name: str,
    root_id: str,
    includes_health_check: bool,
    nickname: str,
    url: str,
    use_vpn: bool,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateGitRoot (
            $branch: String!
            $environment: String!
            $gitignore: [String!]!
            $groupName: String!
            $id: ID!
            $includesHealthCheck: Boolean!
            $nickname: String
            $url: String!
            $useVpn: Boolean!
        ) {
        updateGitRoot(
            branch: $branch
            environment: $environment
            gitignore: $gitignore
            groupName: $groupName
            id: $id
            includesHealthCheck: $includesHealthCheck
            nickname: $nickname
            url: $url
            useVpn: $useVpn
        ) {
            success
        }
      }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "branch": branch,
            "environment": environment,
            "gitignore": gitignore,
            "groupName": group_name,
            "id": root_id,
            "includesHealthCheck": includes_health_check,
            "nickname": nickname,
            "url": url,
            "useVpn": use_vpn,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding(
    *,
    user: str,
    finding_id: str,
) -> dict[str, Any]:
    query: str = """
        query GetFindingNzrVulns(
            $after: String
            $findingId: String!
            $first: Int
            $state: VulnerabilityState
        ) {
            finding(identifier: $findingId) {
                __typename
                id
                where
                vulnerabilitiesConnection(
                    after: $after,
                    first: $first,
                    state: $state
                ) {
                    edges {
                        node {
                            where
                            rootNickname
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "findingId": finding_id,
            "first": 100,
            "state": None,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
