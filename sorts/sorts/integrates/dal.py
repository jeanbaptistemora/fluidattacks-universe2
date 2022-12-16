import functools
from gql import (
    gql,
)
from gql.transport.exceptions import (
    TransportQueryError,
    TransportServerError,
)
from requests.exceptions import (
    ReadTimeout,
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
import time
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)


def retry_on_errors(func: Callable) -> Callable:
    """Decorator to retry the function if an exception is raised."""

    @functools.wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        for _ in range(10):
            try:
                return func(*args, **kwargs)
            except (
                ConnectionError,
                ReadTimeout,
                TransportQueryError,
                TransportServerError,
            ) as exc:
                if "429" in exc.args:
                    time.sleep(60)
                time.sleep(3)
        return func(*args, **kwargs)

    return decorated


@retry_on_errors
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
        except (
            ConnectionError,
            ReadTimeout,
            TransportQueryError,
            TransportServerError,
        ) as exc:
            log_exception("error", exc)
            log("debug", "query %s: %s", operation, query)
            log("debug", "variables: %s", variables)
            raise exc
    return response


def get_vulnerabilities(finding_id: str) -> List[Vulnerability]:
    """Fetches all reported vulnerabilities in a finding, open or closed"""
    vulnerabilities: List[Vulnerability] = []
    query = """
        query SortsGetVulnerabilities(
            $after: String
            $finding_id: String!
            $first: Int
        ) {
            finding(identifier: $finding_id) {
                id
                title
                vulnerabilitiesConnection(
                    after: $after,
                    first: $first,
                ) {
                    edges {
                        node {
                            currentState
                            vulnerabilityType
                            where
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    """
    result = _execute(
        query=query,
        operation="SortsGetVulnerabilities",
        variables=dict(finding_id=finding_id),
    )

    while True:
        has_next_page = False
        if result:
            vulnerabilities_connection = result["finding"][
                "vulnerabilitiesConnection"
            ]
            vulnerability_page_info = vulnerabilities_connection["pageInfo"]
            vulnerability_edges = vulnerabilities_connection["edges"]
            has_next_page = vulnerability_page_info["hasNextPage"]
            end_cursor = vulnerability_page_info["endCursor"]
            vulnerabilities.extend(
                [
                    Vulnerability(
                        current_state=vuln_edge["node"]["currentState"],
                        kind=VulnerabilityKindEnum(
                            vuln_edge["node"]["vulnerabilityType"]
                        ),
                        title=result["finding"]["title"],
                        where=vuln_edge["node"]["where"],
                    )
                    for vuln_edge in vulnerability_edges
                ]
            )

        if not has_next_page:
            break

        result = _execute(
            query=query,
            operation="SortsGetVulnerabilities",
            variables=dict(
                finding_id=finding_id,
                after=end_cursor,
            ),
        )

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
                    toeLines(bePresent:true) {
                        edges {
                            node {
                                attackedLines
                                filename
                                loc
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
                        attacked_lines=edge["node"].get("attackedLines", 0),
                        filename=edge["node"].get("filename", ""),
                        loc=edge["node"].get("loc", 0),
                        root_nickname=edge["node"]["root"].get("nickname", ""),
                        sorts_risk_level=edge["node"].get(
                            "sortsRiskLevel", ""
                        ),
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
                        toeLines(bePresent:true after: $after) {
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
    group_name: str,
    root_nickname: str,
    filename: str,
    risk_level_date: str,
    risk_level: Optional[int] = None,
) -> bool:
    result = _execute(
        query="""
            mutation SortsUpdateToeLinesSorts(
                $group_name: String!,
                $root_nickname: String!,
                $filename: String!,
                $risk_level: Int,
                $risk_level_date: DateTime!
            ) {
                updateToeLinesSorts(
                    groupName: $group_name,
                    rootNickname: $root_nickname,
                    filename: $filename,
                    sortsRiskLevel: $risk_level
                    sortsRiskLevelDate: $risk_level_date
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
            risk_level_date=risk_level_date,
        ),
    )

    if not result:
        return False

    return result["updateToeLinesSorts"]["success"]


def update_toe_lines_suggestions(
    group_name: str,
    root_nickname: str,
    filename: str,
    sorts_suggestions: List[Dict],
) -> bool:
    result = _execute(
        query="""
            mutation SortsUpdateToeLinesSorts(
                $group_name: String!,
                $root_nickname: String!,
                $filename: String!,
                $sorts_suggestions: [SortsSuggestionInput!]
            ) {
                updateToeLinesSorts(
                    groupName: $group_name,
                    rootNickname: $root_nickname,
                    filename: $filename,
                    sortsSuggestions: $sorts_suggestions
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
            sorts_suggestions=sorts_suggestions,
        ),
    )

    return result["updateToeLinesSorts"]["success"]


def get_finding_ids(group: str) -> List[str]:
    """Fetches all finding ids for a group"""
    finding_ids: List[str] = []
    result = _execute(
        query="""
            query SortsGetFindingIds(
                $group: String!
            ) {
                group(groupName: $group) {
                    findings {
                        id
                    }
                }
            }
        """,
        operation="SortsGetFindingIds",
        variables=dict(
            group=group,
        ),
    )

    if result:
        finding_ids = [
            finding["id"] for finding in result["group"]["findings"]
        ]
    return finding_ids
