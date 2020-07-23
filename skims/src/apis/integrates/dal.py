# Standard library
from typing import (
    Any,
    Dict,
    NamedTuple,
    Tuple,
)

# Local libraries
from apis.integrates.graphql import (
    Session,
)
from model import (
    FindingEnum,
    KindEnum,
    Vulnerability,
    VulnerabilityStateEnum,
)
from utils.function import (
    retry,
)
from utils.logs import (
    log,
)
from utils.string import (
    to_in_memory_file,
)


async def _execute(*, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    response = await Session.value.execute(query=query, variables=variables)

    result: Dict[str, Any] = await response.json()

    if 'errors' in result:
        await log('error', '%s', result)

    return result


@retry()
async def get_group_level_role(
    *,
    group: str,
) -> str:
    result = await _execute(
        query="""
            query GetGroupLevelRole(
                $group: String!
            ) {
                me {
                    role(
                        entity: PROJECT
                        identifier: $group
                    )
                }
            }
        """,
        variables=dict(
            group=group,
        )
    )

    role: str = result['data']['me']['role']

    return role


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


@retry()
async def get_group_findings(
    *,
    group: str,
) -> Tuple[ResultGetGroupFindings, ...]:
    result = await _execute(
        query="""
            query GetGroupFindings(
                $group: String!
            ) {
                project(projectName: $group) {
                    findings {
                        id
                        title
                    }
                }
            }
        """,
        variables=dict(
            group=group,
        )
    )

    return tuple(
        ResultGetGroupFindings(
            identifier=finding['id'],
            title=finding['title'],
        )
        for finding in result['data']['project']['findings']
    )


@retry()
async def get_finding_vulnerabilities(
    *,
    finding: FindingEnum,
    finding_id: str,
) -> Tuple[Vulnerability, ...]:
    result = await _execute(
        query="""
            query GetFindingVulnerabilities(
                $finding_id: String!
            ) {
                finding(identifier: $finding_id) {
                    vulnerabilities {
                        currentState
                        specific
                        vulnType
                        where
                    }
                }
            }
        """,
        variables=dict(
            finding_id=finding_id,
        )
    )

    return tuple(
        Vulnerability(
            finding=finding,
            kind=KindEnum(vulnerability['vulnType']),
            state=VulnerabilityStateEnum(vulnerability['currentState']),
            what=vulnerability['where'],
            where=vulnerability['specific'],
        )
        for vulnerability in result['data']['finding']['vulnerabilities']
    )


@retry()
async def do_upload_vulnerabilities(
    *,
    finding_id: str,
    stream: str,
) -> bool:
    result = await _execute(
        query="""
            mutation DoUploadFile(
                $file_handle: Upload!
                $finding_id: String!
            ) {
                uploadFile(
                    findingId: $finding_id
                    file: $file_handle
                ) {
                    success
                }
            }
        """,
        variables=dict(
            file_handle=await to_in_memory_file(stream),
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['uploadFile']['success']

    return success
