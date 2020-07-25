# Standard library
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
    Tuple,
    Type,
)

# Local libraries
from integrates.graphql import (
    Session,
)
from utils.function import (
    retry,
)
from utils.logs import (
    log,
)
from utils.model import (
    FindingEnum,
    IntegratesVulnerabilityMetadata,
    SeverityEnum,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_in_memory_file,
)


class ErrorMapping(NamedTuple):
    exception_cls: Type[Exception]
    exception_msg: str
    messages: Tuple[str, ...]


async def raise_errors(
    errors: Optional[Tuple[Dict[str, Any], ...]],
    error_mappings: Tuple[ErrorMapping, ...],
) -> None:
    for error in (errors or ()):
        for error_mapping in error_mappings:
            if error.get('message') in error_mapping.messages:
                raise error_mapping.exception_cls(
                    error_mapping.exception_msg,
                )

    if errors:
        for error in errors:
            await log('error', '%s', error)
    else:
        # no errors happened
        pass


async def _execute(*, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    response = await Session.value.execute(query=query, variables=variables)

    result: Dict[str, Any] = await response.json()

    await raise_errors(
        errors=result.get('errors'),
        error_mappings=(
            ErrorMapping(
                exception_cls=PermissionError,
                exception_msg='Invalid API token',
                messages=(
                    'Login required',
                ),
            ),
            ErrorMapping(
                exception_cls=PermissionError,
                exception_msg='Access denied',
                messages=(
                    'Access denied',
                ),
            ),
        ),
    )

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

    role: str = result['data']['me']['role'] or 'none'

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
                    drafts {
                        id
                        title
                    }
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
        for finding in (
            result['data']['project']['drafts'] +
            result['data']['project']['findings']
        )
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
                        currentApprovalStatus
                        currentState
                        id
                        source
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
            integrates_metadata=IntegratesVulnerabilityMetadata(
                approval_status=VulnerabilityApprovalStatusEnum((
                    vulnerability['currentApprovalStatus'] or
                    VulnerabilityApprovalStatusEnum.APPROVED
                )),
                source=VulnerabilitySourceEnum(vulnerability['source']),
                uuid=vulnerability['id'],
            ),
            kind=VulnerabilityKindEnum(vulnerability['vulnType']),
            state=VulnerabilityStateEnum(vulnerability['currentState']),
            what=vulnerability['where'],
            where=vulnerability['specific'],
        )
        for vulnerability in result['data']['finding']['vulnerabilities']
    )


@retry()
async def do_release_vulnerability(
    *,
    finding_id: str,
    vulnerability_uuid: str,
) -> bool:
    result = await _execute(
        query="""
            mutation DoReleaseVulnerability(
                $finding_id: String!
                $vulnerability_uuid: String!
            ) {
                approveVulnerability(
                    approvalStatus: true
                    findingId: $finding_id
                    uuid: $vulnerability_uuid
                ) {
                    success
                }
            }
        """,
        variables=dict(
            finding_id=finding_id,
            vulnerability_uuid=vulnerability_uuid,
        )
    )

    success: bool = result['data']['approveVulnerability']['success']

    return success


@retry()
async def do_create_draft(
    *,
    finding: FindingEnum,
    group: str,
) -> bool:
    result = await _execute(
        query="""
            mutation DoCreateDraft(
                $group: String!
                $title: String!
            ) {
                createDraft(
                    projectName: $group,
                    title: $title,
                ) {
                    success
                }
            }
        """,
        variables=dict(
            group=group,
            title=finding.value,
        )
    )

    success: bool = result['data']['createDraft']['success']

    return success


@retry()
async def do_delete_finding(
    *,
    finding_id: str,
) -> bool:
    await log('warn', 'Deleting finding: %s', finding_id)

    result = await _execute(
        query="""
            mutation DoDeleteFinding(
                $finding_id: String!
            ) {
                deleteFinding(
                    findingId: $finding_id
                    justification: NOT_REQUIRED
                ) {
                    success
                }
            }
        """,
        variables=dict(
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['deleteFinding']['success']

    await log('warn', 'Deleting finding: %s, success: %s', finding_id, success)

    return success


@retry()
async def do_update_finding_severity(
    *,
    finding_id: str,
    severity: SeverityEnum,
) -> bool:
    result = await _execute(
        query="""
            mutation DoUpdateSeverity(
                $finding_id: String!
                $data: GenericScalar!
            ) {
                updateSeverity(
                    findingId: $finding_id
                    data: $data
                ) {
                    success
                }
            }
        """,
        variables=dict(
            finding_id=finding_id,
            data=dict(
                cvssVersion='3.1',
                id=finding_id,
                **severity.value,
            ),
        )
    )

    success: bool = result['data']['updateSeverity']['success']

    return success


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
