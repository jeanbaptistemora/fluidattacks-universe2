# Standard library
from io import (
    BytesIO,
)
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
)

# Third party libraries
import aiohttp

# Local libraries
from integrates.graphql import (
    Session,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
from utils.function import (
    shield,
    RetryAndFinallyReturn,
    StopRetrying,
)
from utils.logs import (
    log,
)
from utils.model import (
    FindingEnum,
    FindingEvidenceIDEnum,
    FindingEvidenceDescriptionIDEnum,
    FindingReleaseStatusEnum,
    IntegratesVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_in_memory_file,
)
from zone import (
    t,
)


# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=12,
    sleep_between_retries=5,
)


class ErrorMapping(NamedTuple):
    exception: Exception
    messages: Tuple[str, ...]


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
    else:
        # no errors happened
        pass


async def _execute(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
) -> Dict[str, Any]:
    response: aiohttp.ClientResponse = await Session.value.execute(
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
async def get_group_level_role(
    *,
    group: str,
) -> str:
    result = await _execute(
        query="""
            query SkimsGetGroupLevelRole(
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
        operation='SkimsGetGroupLevelRole',
        variables=dict(
            group=group,
        )
    )

    role: str = result['data']['me']['role'] or 'none'

    return role


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


@SHIELD
async def get_group_findings(
    *,
    group: str,
) -> Tuple[ResultGetGroupFindings, ...]:
    result = await _execute(
        query="""
            query SkimsGetGroupFindings(
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
        operation='SkimsGetGroupFindings',
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
            result['data']['project']['findings'] +
            result['data']['project']['drafts']
        )
    )


@SHIELD
async def get_finding_current_release_status(
    *,
    finding_id: str,
) -> FindingReleaseStatusEnum:
    result = await _execute(
        query="""
            query SkimsGetFindingCurrentReleaseStatus(
                $finding_id: String!
            ) {
                finding(identifier: $finding_id) {
                    currentState
                }
            }
        """,
        operation='SkimsGetFindingCurrentReleaseStatus',
        variables=dict(
            finding_id=finding_id,
        )
    )

    return (
        FindingReleaseStatusEnum(result['data']['finding']['currentState'])
        if result['data']['finding']['currentState']
        else FindingReleaseStatusEnum.APPROVED
    )


@SHIELD
async def get_finding_vulnerabilities(
    *,
    finding: FindingEnum,
    finding_id: str,
) -> EphemeralStore:
    result = await _execute(
        query="""
            query SkimsGetFindingVulnerabilities(
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
        operation='SkimsGetFindingVulnerabilities',
        variables=dict(
            finding_id=finding_id,
        )
    )

    store: EphemeralStore = get_ephemeral_store()
    for vulnerability in result['data']['finding']['vulnerabilities']:
        await store.store(Vulnerability(
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
        ))

    return store


@SHIELD
async def do_release_vulnerability(
    *,
    finding_id: str,
    vulnerability_uuid: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoReleaseVulnerability(
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
        operation='SkimsDoReleaseVulnerability',
        variables=dict(
            finding_id=finding_id,
            vulnerability_uuid=vulnerability_uuid,
        )
    )

    success: bool = result['data']['approveVulnerability']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_release_vulnerabilities(
    *,
    finding_id: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoReleaseVulnerabilities(
                $finding_id: String!
            ) {
                approveVulnerability(
                    approvalStatus: true
                    findingId: $finding_id
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoReleaseVulnerabilities',
        variables=dict(
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['approveVulnerability']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_create_draft(
    *,
    affected_systems: str,
    finding: FindingEnum,
    group: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoCreateDraft(
                $affected_systems: String
                $impact: String
                $cwe: String
                $description: String
                $group: String!
                $recommendation: String
                $requirements: String
                $threat: String
                $title: String!
                $type: FindingType
            ) {
                createDraft(
                    affectedSystems: $affected_systems
                    attackVectorDesc: $impact
                    cwe: $cwe
                    description: $description
                    projectName: $group
                    recommendation: $recommendation
                    requirements: $requirements
                    threat: $threat
                    title: $title
                    type: $type
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoCreateDraft',
        variables=dict(
            affected_systems=affected_systems,
            cwe=finding.value.cwe,
            description=t(finding.value.description),
            impact=t(finding.value.impact),
            group=group,
            recommendation=t(finding.value.recommendation),
            requirements=t(finding.value.requirements),
            threat=t(finding.value.threat),
            title=t(finding.value.title),
            type=finding.value.type.value,
        )
    )

    success: bool = result['data']['createDraft']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_delete_finding(
    *,
    finding_id: str,
) -> bool:
    await log('warn', 'Deleting finding: %s', finding_id)

    result = await _execute(
        query="""
            mutation SkimsDoDeleteFinding(
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
        operation='SkimsDoDeleteFinding',
        variables=dict(
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['deleteFinding']['success']

    await log('warn', 'Deleting finding: %s, success: %s', finding_id, success)

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_approve_draft(
    *,
    finding_id: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoApproveDraft(
                $finding_id: String!
            ) {
                approveDraft(
                    draftId: $finding_id
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoApproveDraft',
        variables=dict(
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['approveDraft']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_submit_draft(
    *,
    finding_id: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoSubmitDraft(
                $finding_id: String!
            ) {
                submitDraft(
                    findingId: $finding_id
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoSubmitDraft',
        variables=dict(
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['submitDraft']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_update_finding_severity(
    *,
    finding_id: str,
    severity: Dict[str, float],
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoUpdateFindingSeverity(
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
        operation='SkimsDoUpdateFindingSeverity',
        variables=dict(
            finding_id=finding_id,
            data=dict(
                cvssVersion='3.1',
                id=finding_id,
                **severity,
            ),
        )
    )

    success: bool = result['data']['updateSeverity']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_update_evidence(
    *,
    evidence_id: FindingEvidenceIDEnum,
    evidence_stream: bytes,
    finding_id: str,
) -> bool:
    evidence_buffer = BytesIO(evidence_stream)

    result = await _execute(
        query="""
            mutation SkimsDoUpdateEvidence(
                $evidence_id: EvidenceType!
                $evidence_buffer: Upload!
                $finding_id: String!
            ) {
                updateEvidence(
                    evidenceId: $evidence_id
                    file: $evidence_buffer
                    findingId: $finding_id
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoUpdateEvidence',
        variables=dict(
            evidence_id=evidence_id.value,
            evidence_buffer=evidence_buffer,
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['updateEvidence']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_update_evidence_description(
    *,
    evidence_description: str,
    evidence_description_id: FindingEvidenceDescriptionIDEnum,
    finding_id: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoUpdateEvidenceDescription(
                $evidence_description: String!
                $evidence_description_id: EvidenceDescriptionType!
                $finding_id: String!
            ) {
                updateEvidenceDescription(
                    description: $evidence_description
                    evidenceId: $evidence_description_id
                    findingId: $finding_id
                ) {
                    success
                }
            }
        """,
        operation='SkimsDoUpdateEvidenceDescription',
        variables=dict(
            evidence_description=evidence_description,
            evidence_description_id=evidence_description_id.value,
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['updateEvidenceDescription']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_upload_vulnerabilities(
    *,
    finding_id: str,
    stream: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoUploadVulnerabilities(
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
        operation='SkimsDoUploadVulnerabilities',
        variables=dict(
            file_handle=await to_in_memory_file(stream),
            finding_id=finding_id,
        )
    )

    success: bool = result['data']['uploadFile']['success']

    if not success:
        raise RetryAndFinallyReturn(success)

    return success
