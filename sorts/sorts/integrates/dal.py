# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Tuple,
    TypeVar,
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


# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


class ErrorMapping(NamedTuple):
    exception: Exception
    messages: Tuple[str, ...]


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
    response: Dict[str, Any] = {}
    with graphql_client() as client:
        try:
            response = client.execute(gql(query), variables)
        except TransportQueryError as exc:
            log_exception('error', exc)
            log('debug', 'query %s: %s', operation, query)
            log('debug', 'variables: %s', variables)
    return response


def get_vulnerabilities(group: str) -> List[Vulnerability]:
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
