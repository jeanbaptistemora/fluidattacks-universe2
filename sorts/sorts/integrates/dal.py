# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
)

# Third-party libraries
import aiohttp

# Local libraries
from integrates.graphql import client as graphql_client
from utils.decorators import (
    shield,
    StopRetrying,
)
from utils.logs import log


# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(retries=3)


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


async def raise_errors(
    errors: Optional[Tuple[Dict[str, Any], ...]],
    error_mappings: Tuple[ErrorMapping, ...],
    query: str,
    variables: Dict[str, Any],
) -> None:
    for error in (errors or ()):
        for error_mapping in error_mappings:
            if error.get('message') in error_mapping.messages:
                raise error_mapping.exception

    if errors:
        for error in errors:
            await log('debug', 'query: %s', query)
            await log('debug', 'variables: %s', variables)
            await log('error', '%s', error)


async def _execute(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
) -> Dict[str, Any]:
    async with graphql_client() as client:
        response: aiohttp.ClientResponse = await client.execute(
            query=query,
            operation=operation,
            variables=variables,
        )

        if response.status >= 400:
            await log('debug', 'query: %s', query)
            await log('debug', 'variables: %s', variables)
            await log('debug', 'response status: %s', response.status)
            raise aiohttp.ClientError()

        result: Dict[str, Any] = await response.json()

    await raise_errors(
        errors=result.get('errors'),
        error_mappings=(
            ErrorMapping(
                exception=StopRetrying('Invalid API token'),
                messages=(
                    'Login required',
                ),
            ),
            ErrorMapping(
                exception=StopRetrying('Access denied'),
                messages=(
                    'Access denied',
                ),
            ),
        ),
        query=query,
        variables=variables,
    )

    return result


@SHIELD
async def get_vulnerabilities(group: str) -> List[Vulnerability]:
    result = await _execute(
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

    vulnerabilities: List[Vulnerability] = [
        Vulnerability(
            kind=VulnerabilityKindEnum(vuln['vulnType']),
            where=vuln['where']
        )
        for finding in result['data']['project']['findings']
        for vuln in finding['vulnerabilities']
    ]
    return vulnerabilities
