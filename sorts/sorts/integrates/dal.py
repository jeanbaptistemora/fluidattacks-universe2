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
        variables=dict(),
    )

    return result["me"]["userEmail"]


def get_toe_lines_sorts(group_name: str) -> List[ToeLines]:
    group_toe_lines: List[ToeLines] = []
    result = _execute(
        query="""
            query GetToeLines($group_name: String!) {
                group(groupName: $group_name) {
                    name
                    roots {
                        ... on GitRoot {
                            toeLines {
                                filename
                                sortsRiskLevel
                            }
                        }
                    }
                }
            }
        """,
        operation="GetToeLines",
        variables=dict(group_name=group_name),
    )

    if result:
        group_roots = result["group"]["roots"]
        group_toe_lines = [
            ToeLines(
                filename=toe_lines["filename"],
                sorts_risk_level=toe_lines["sortsRiskLevel"],
            )
            for group_root in group_roots
            for toe_lines in group_root["toeLines"]
        ]

    return group_toe_lines


def update_toe_lines_sorts(
    group_name: str, filename: str, risk_level: int
) -> bool:
    result = _execute(
        query="""
            mutation SortsUpdateToeLinesSorts(
                $group_name: String!,
                $filename: String!,
                $risk_level: Int!
            ) {
                updateToeLinesSorts(
                    groupName: $group_name,
                    filename: $filename,
                    sortsRiskLevel: $risk_level
                ) {
                    success
                }
            }
        """,
        operation="SortsUpdateToeLinesSorts",
        variables=dict(
            group_name=group_name, filename=filename, risk_level=risk_level
        ),
    )

    return result["updateToeLinesSorts"]["success"]
