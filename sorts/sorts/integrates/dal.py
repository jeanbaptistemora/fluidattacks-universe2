from gql import (
    gql,
)
from gql.transport.exceptions import (
    TransportQueryError,
)
from sorts.integrates.graphql import (
    client as graphql_client,
)
from sorts.integrates.typing import (
    ToeLines,
    Vulnerability,
    VulnerabilityKindEnum,
)
from sorts.utils.logs import (
    log,
    log_exception,
)
from typing import (
    Any,
    Dict,
    List,
)


def _execute(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
) -> Dict[str, Any]:
    """Sends query to the backend"""
    response: Dict[str, Any] = {}
    with graphql_client() as client:
        try:
            response = client.execute(
                document=gql(query),
                variable_values=variables,
                operation_name=operation,
            )
        except TransportQueryError as exc:
            log_exception("error", exc)
            log("debug", "query %s: %s", operation, query)
            log("debug", "variables: %s", variables)
    return response


def get_vulnerabilities(group: str) -> List[Vulnerability]:
    """Fetches all the vulnerabilities reported in a group"""
    vulnerabilities: List[Vulnerability] = []
    result = _execute(
        query="""
            query SortsGetVulnerabilities(
                $group: String!
            ) {
                group(groupName: $group) {
                    findings {
                        id
                        vulnerabilities(state: "open") {
                            vulnerabilityType
                            where
                            historicState
                        }
                    }
                }
            }
        """,
        operation="SortsGetVulnerabilities",
        variables=dict(
            group=group,
        ),
    )

    if result:
        vulnerabilities = [
            Vulnerability(
                kind=VulnerabilityKindEnum(vuln["vulnerabilityType"]),
                source=vuln["historicState"][0]["source"],
                where=vuln["where"],
            )
            for finding in result["group"]["findings"]
            for vuln in finding["vulnerabilities"]
        ]
    return vulnerabilities


def get_user_email() -> str:
    result = _execute(
        query="""
            query SortsGetUserInfo {
                me {
                    userEmail
                }
            }
        """,
        operation="SortsGetUserInfo",
        variables={},
    )

    return result["me"]["userEmail"]


def get_toe_lines_sorts(group_name: str) -> List[ToeLines]:
    group_toe_lines: List[ToeLines] = []
    result = _execute(
        query="""
            query SortsGetToeLines($group_name: String!) {
                group(groupName: $group_name) {
                    name
                    toeLines {
                        edges {
                            node {
                                filename
                                root {
                                    nickname
                                }
                                sortsRiskLevel
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """,
        operation="SortsGetToeLines",
        variables=dict(group_name=group_name),
    )
    while True:
        has_next_page = False
        if result:
            toe_lines_edges = result["group"]["toeLines"]["edges"]
            has_next_page = result["group"]["toeLines"]["pageInfo"][
                "hasNextPage"
            ]
            end_cursor = result["group"]["toeLines"]["pageInfo"]["endCursor"]
            group_toe_lines.extend(
                [
                    ToeLines(
                        filename=edge["node"]["filename"],
                        root_nickname=edge["node"]["root"]["nickname"],
                        sorts_risk_level=edge["node"]["sortsRiskLevel"],
                    )
                    for edge in toe_lines_edges
                ]
            )

        if has_next_page:
            result = _execute(
                query="""
                query SortsGetToeLines($group_name: String!, $after: String!) {
                    group(groupName: $group_name) {
                        name
                        toeLines(after: $after) {
                            edges {
                                node {
                                    filename
                                    root {
                                        nickname
                                    }
                                    sortsRiskLevel
                                }
                            }
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                        }
                    }
                }
            """,
                operation="SortsGetToeLines",
                variables=dict(group_name=group_name, after=end_cursor),
            )
        else:
            break
    return group_toe_lines


def update_toe_lines_sorts(
    group_name: str, root_nickname: str, filename: str, risk_level: int
) -> bool:
    result = _execute(
        query="""
            mutation SortsUpdateToeLinesSorts(
                $group_name: String!,
                $root_nickname: String!,
                $filename: String!,
                $risk_level: Int!
            ) {
                updateToeLinesSorts(
                    groupName: $group_name,
                    rootNickname: $root_nickname,
                    filename: $filename,
                    sortsRiskLevel: $risk_level
                ) {
                    success
                }
            }
        """,
        operation="SortsUpdateToeLinesSorts",
        variables=dict(
            group_name=group_name,
            root_nickname=root_nickname,
            filename=filename,
            risk_level=risk_level,
        ),
    )

    return result["updateToeLinesSorts"]["success"]
