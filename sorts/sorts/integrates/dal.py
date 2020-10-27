# Standard libraries
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)

# Third-party libraries
from gql import gql
from gql.transport.exceptions import TransportQueryError

# Local libraries
from integrates.graphql import client as graphql_client
from utils.logs import (
    log,
    log_exception,
)


class VulnerabilityKindEnum(Enum):
    INPUTS: str = 'inputs'
    LINES: str = 'lines'
    PORTS: str = 'ports'


class Vulnerability(NamedTuple):
    kind: VulnerabilityKindEnum
    where: str


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
                operation_name=operation
            )
        except TransportQueryError as exc:
            log_exception('error', exc)
            log('debug', 'query %s: %s', operation, query)
            log('debug', 'variables: %s', variables)
    return response


def get_vulnerabilities(group: str) -> List[Vulnerability]:
    """Fetches all the vulnerabilities reported in a group"""
    vulnerabilities: List[Vulnerability] = []
    result = _execute(
        query="""
            query SortsGetVulnerabilities(
                $group: String!
            ) {
                project(projectName: $group) {
                    findings {
                        id
                        vulnerabilities(state: "open") {
                            vulnType
                            where
                        }
                    }
                }
            }
        """,
        operation='SortsGetVulnerabilities',
        variables=dict(
            group=group,
        )
    )

    if result:
        vulnerabilities = [
            Vulnerability(
                kind=VulnerabilityKindEnum(vuln['vulnType']),
                where=vuln['where']
            )
            for finding in result['project']['findings']
            for vuln in finding['vulnerabilities']
        ]
    return vulnerabilities
