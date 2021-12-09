import aiohttp
from integrates.graphql import (
    client as graphql_client,
)
from io import (
    BytesIO,
)
from model import (
    core_model,
)
from operator import (
    attrgetter,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
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
from utils.function import (
    rate_limited,
    RetryAndFinallyReturn,
    shield,
    SkimsCanNotOperate,
    StopRetrying,
)
from utils.limits import (
    INTEGRATES_DEFAULT as DEFAULT_RATE_LIMIT,
    INTEGRATES_DO_UPDATE_EVIDENCE as DO_UPDATE_EVIDENCE_RATE_LIMIT,
)
from utils.logs import (
    log,
)
from utils.string import (
    to_in_memory_file,
)
from zone import (
    t,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(retries=12)


class ErrorMapping(NamedTuple):
    exception: Exception
    messages: Tuple[str, ...]


async def raise_errors(
    errors: Optional[Tuple[Dict[str, Any], ...]],
    error_mappings: Tuple[ErrorMapping, ...],
    query: str,
    variables: Dict[str, Any],
) -> None:
    for error in errors or ():
        for error_mapping in error_mappings:
            if error.get("message") in error_mapping.messages:
                raise error_mapping.exception

    if errors:
        for error in errors:
            await log("debug", "query: %s", query)
            await log("debug", "variables: %s", variables)
            await log("error", "%s", error)
    else:
        # no errors happened
        pass


@rate_limited(rpm=DEFAULT_RATE_LIMIT)
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
            await log("debug", "query: %s", query)
            await log("debug", "variables: %s", variables)
            await log("debug", "response status: %s", response.status)
            raise aiohttp.ClientError()

        result: Dict[str, Any] = await response.json()

    await raise_errors(
        errors=result.get("errors"),
        error_mappings=(
            ErrorMapping(
                exception=StopRetrying("Invalid API token"),
                messages=("Login required",),
            ),
            ErrorMapping(
                exception=SkimsCanNotOperate(),
                messages=("Exception - Machine cannot operate at this time",),
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
                group(groupName: $group){
                    userRole
                }
            }
        """,
        operation="SkimsGetGroupLevelRole",
        variables=dict(
            group=group,
        ),
    )

    role: str = result["data"]["group"]["userRole"] or "none"

    return role


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


async def get_group_finding_ids(group: str) -> Tuple[str, ...]:
    return tuple(
        map(attrgetter("identifier"), await get_group_findings(group=group)),
    )


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
                group(groupName: $group) {
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
        operation="SkimsGetGroupFindings",
        variables=dict(
            group=group,
        ),
    )

    findings: List[ResultGetGroupFindings] = [
        ResultGetGroupFindings(
            identifier=finding["id"],
            title=finding["title"],
        )
        for finding in (
            result["data"]["group"]["findings"]
            + result["data"]["group"]["drafts"]
        )
    ]

    findings = sorted(
        findings,
        key=lambda result: (result.title, result.identifier),
    )

    return tuple(findings)


@SHIELD
async def get_group_language(group: str) -> core_model.LocalesEnum:
    result = await _execute(
        query="""
            query SkimsGetGroupLanguage($group: String!) {
                group(groupName: $group) {
                    language
                }
            }
        """,
        operation="SkimsGetGroupLanguage",
        variables=dict(group=group),
    )

    return core_model.LocalesEnum(result["data"]["group"]["language"])


@SHIELD
async def get_group_open_severity(group: str) -> float:
    result = await _execute(
        query="""
            query SkimsGetGroupOpenSeverity($group: String!) {
                group(groupName: $group) {
                    findings {
                        openVulnerabilities
                        severityScore
                    }
                }
            }
        """,
        operation="SkimsGetGroupOpenSeverity",
        variables=dict(group=group),
    )

    return sum(
        finding["openVulnerabilities"] * (4 ** (finding["severityScore"] - 4))
        for finding in result["data"]["group"]["findings"]
    )


class ResultGetGroupRoots(NamedTuple):
    environment_urls: List[str]
    nickname: str


@SHIELD
async def get_group_roots(
    *,
    group: str,
) -> Tuple[ResultGetGroupRoots, ...]:
    result = await _execute(
        query="""
            query SkimsGetGroupRoots(
                $group: String!
            ) {
                group(groupName: $group) {
                    roots {
                        ... on GitRoot {
                            environmentUrls
                            nickname
                        }
                    }
                }
            }
        """,
        operation="SkimsGetGroupRoots",
        variables=dict(
            group=group,
        ),
    )

    return tuple(
        ResultGetGroupRoots(
            environment_urls=root["environmentUrls"],
            nickname=root["nickname"],
        )
        for root in result["data"]["group"]["roots"]
    )


@SHIELD
async def get_finding_current_release_status(
    *,
    finding_id: str,
) -> core_model.FindingReleaseStatusEnum:
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
        operation="SkimsGetFindingCurrentReleaseStatus",
        variables=dict(
            finding_id=finding_id,
        ),
    )

    return (
        core_model.FindingReleaseStatusEnum(
            result["data"]["finding"]["currentState"]
        )
        if result["data"]["finding"]["currentState"]
        else core_model.FindingReleaseStatusEnum.APPROVED
    )


@SHIELD
async def get_finding_vulnerabilities(
    *,
    finding: core_model.FindingEnum,
    finding_id: str,
) -> EphemeralStore:
    result = await _execute(
        query="""
            query SkimsGetFindingVulnerabilities(
                $finding_id: String!
            ) {
                finding(identifier: $finding_id) {
                    vulnerabilities {
                        commitHash
                        currentState
                        historicState
                        historicVerification {
                            date
                            status
                        }
                        id
                        specific
                        stream
                        vulnerabilityType
                        where
                    }
                }
            }
        """,
        operation="SkimsGetFindingVulnerabilities",
        variables=dict(
            finding_id=finding_id,
        ),
    )

    store: EphemeralStore = get_ephemeral_store()
    for vulnerability in result["data"]["finding"]["vulnerabilities"]:
        kind = core_model.VulnerabilityKindEnum(
            vulnerability["vulnerabilityType"]
        )
        namespace, what = core_model.Vulnerability.what_from_integrates(
            kind=kind,
            what_on_integrates=vulnerability["where"],
        )
        source = core_model.VulnerabilitySourceEnum.from_historic(
            vulnerability["historicState"],
        )
        verification = core_model.VulnerabilityVerification.from_historic(
            vulnerability["historicVerification"],
        )
        stream = vulnerability["stream"]
        if stream is not None:
            stream = stream.replace(" > ", ",")

        await store.store(
            core_model.Vulnerability(
                finding=finding,
                integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                    commit_hash=vulnerability["commitHash"],
                    source=source,
                    verification=verification,
                    uuid=vulnerability["id"],
                ),
                kind=kind,
                namespace=namespace,
                state=core_model.VulnerabilityStateEnum(
                    vulnerability["currentState"]
                ),
                stream=stream,
                what=what,
                where=vulnerability["specific"],
            )
        )

    return store


@SHIELD
async def do_add_git_root(
    *,
    branch: str = "main",
    environment: str = "production",
    gitignore: Optional[List[str]] = None,
    group_name: str,
    includes_health_check: bool = False,
    nickname: str,
    url: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoAddGitRoot(
                $branch: String!
                $environment: String!
                $gitignore: [String!]!
                $groupName: String!
                $includesHealthCheck: Boolean!
                $nickname: String
                $url: String!
            ) {
                addGitRoot(
                    branch: $branch
                    environment: $environment
                    gitignore: $gitignore
                    groupName: $groupName
                    includesHealthCheck: $includesHealthCheck
                    nickname: $nickname
                    url: $url
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoAddGitRoot",
        variables=dict(
            branch=branch,
            environment=environment,
            gitignore=gitignore or [],
            groupName=group_name,
            includesHealthCheck=includes_health_check,
            nickname=nickname,
            url=url,
        ),
    )

    success: bool = result["data"]["addGitRoot"]["success"]

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_create_draft(
    *,
    affected_systems: str,
    finding: core_model.FindingEnum,
    group: str,
) -> bool:
    try:
        result = await _execute(
            query="""
            mutation SkimsDoAddDraft(
                $affected_systems: String
                $impact: String
                $description: String
                $group: String!
                $recommendation: String
                $requirements: String
                $threat: String
                $title: String!
            ) {
                addDraft(
                    affectedSystems: $affected_systems
                    attackVectorDescription: $impact
                    description: $description
                    groupName: $group
                    recommendation: $recommendation
                    requirements: $requirements
                    threat: $threat
                    title: $title
                ) {
                    success
                }
            }
        """,
            operation="SkimsDoAddDraft",
            variables=dict(
                affected_systems=affected_systems,
                description=t(finding.value.description),
                impact=t(finding.value.impact),
                group=group,
                recommendation=t(finding.value.recommendation),
                requirements="\n".join(
                    t(f"criteria.requirements.{requirement.zfill(3)}")
                    for requirement in map(str, finding.value.requirements)
                ),
                threat=t(finding.value.threat),
                title=t(finding.value.title),
            ),
        )

        success: bool = result["data"]["addDraft"]["success"]
        if not success:
            raise RetryAndFinallyReturn(success)
    except SkimsCanNotOperate:
        return False

    return success


@SHIELD
async def do_delete_finding(
    *,
    finding_id: str,
) -> bool:
    await log("warn", "Deleting finding: %s", finding_id)

    result = await _execute(
        query="""
            mutation SkimsDoRemoveFinding(
                $finding_id: String!
            ) {
                removeFinding(
                    findingId: $finding_id
                    justification: NOT_REQUIRED
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoRemoveFinding",
        variables=dict(
            finding_id=finding_id,
        ),
    )

    success: bool = result["data"]["removeFinding"]["success"]

    await log("warn", "Removing finding: %s, success: %s", finding_id, success)

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_approve_draft(
    *,
    finding_id: str,
) -> bool:
    try:
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
            operation="SkimsDoApproveDraft",
            variables=dict(
                finding_id=finding_id,
            ),
        )

        success: bool = result["data"]["approveDraft"]["success"]

        if not success:
            raise RetryAndFinallyReturn(success)
    except SkimsCanNotOperate:
        return False

    return success


@SHIELD
async def do_submit_draft(
    *,
    finding_id: str,
) -> bool:
    try:
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
            operation="SkimsDoSubmitDraft",
            variables=dict(
                finding_id=finding_id,
            ),
        )

        success: bool = result["data"]["submitDraft"]["success"]

        if not success:
            raise RetryAndFinallyReturn(success)
    except SkimsCanNotOperate:
        return False

    return success


@SHIELD
async def do_update_finding_severity(
    *,
    finding_id: str,
    severity: Dict[str, float],
) -> bool:
    try:
        result = await _execute(
            query="""
            mutation SkimsDoUpdateFindingSeverity(
                $findingId: String!
                $attackComplexity: String!
                $attackVector: String!
                $availabilityImpact: String!
                $availabilityRequirement: String!
                $confidentialityImpact: String!
                $confidentialityRequirement: String!
                $cvssVersion: String!
                $exploitability: String!
                $integrityImpact: String!
                $integrityRequirement: String!
                $modifiedAttackComplexity: String!
                $modifiedAttackVector: String!
                $modifiedAvailabilityImpact: String!
                $modifiedConfidentialityImpact: String!
                $modifiedIntegrityImpact: String!
                $modifiedPrivilegesRequired: String!
                $modifiedSeverityScope: String!
                $modifiedUserInteraction: String!
                $privilegesRequired: String!
                $remediationLevel: String!
                $reportConfidence: String!
                $severity: String
                $severityScope: String!
                $userInteraction: String!
            ) {
                updateSeverity(
                    findingId: $findingId
                    attackComplexity: $attackComplexity
                    attackVector: $attackVector
                    availabilityImpact: $availabilityImpact
                    availabilityRequirement: $availabilityRequirement
                    confidentialityImpact: $confidentialityImpact
                    confidentialityRequirement: $confidentialityRequirement
                    cvssVersion: $cvssVersion
                    exploitability: $exploitability
                    integrityImpact: $integrityImpact
                    integrityRequirement: $integrityRequirement
                    modifiedAttackComplexity: $modifiedAttackComplexity
                    modifiedAttackVector: $modifiedAttackVector
                    modifiedAvailabilityImpact: $modifiedAvailabilityImpact
                    modifiedConfidentialityImpact:
                        $modifiedConfidentialityImpact
                    modifiedIntegrityImpact: $modifiedIntegrityImpact
                    modifiedPrivilegesRequired: $modifiedPrivilegesRequired
                    modifiedSeverityScope: $modifiedSeverityScope
                    modifiedUserInteraction: $modifiedUserInteraction
                    privilegesRequired: $privilegesRequired
                    remediationLevel: $remediationLevel
                    reportConfidence: $reportConfidence
                    severity: $severity
                    severityScope: $severityScope
                    userInteraction: $userInteraction
                ) {
                    success
                }
            }
        """,
            operation="SkimsDoUpdateFindingSeverity",
            variables=dict(
                cvssVersion="3.1", findingId=finding_id, **severity
            ),
        )

        success: bool = result["data"]["updateSeverity"]["success"]

        if not success:
            raise RetryAndFinallyReturn(success)
    except SkimsCanNotOperate:
        return False
    return success


@rate_limited(rpm=DO_UPDATE_EVIDENCE_RATE_LIMIT)
@SHIELD
async def do_update_evidence(
    *,
    evidence_id: core_model.FindingEvidenceIDEnum,
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
        operation="SkimsDoUpdateEvidence",
        variables=dict(
            evidence_id=evidence_id.value,
            evidence_buffer=evidence_buffer,
            finding_id=finding_id,
        ),
    )

    success: bool = result["data"]["updateEvidence"]["success"]

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_update_evidence_description(
    *,
    evidence_description: str,
    evidence_description_id: core_model.FindingEvidenceDescriptionIDEnum,
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
        operation="SkimsDoUpdateEvidenceDescription",
        variables=dict(
            evidence_description=evidence_description,
            evidence_description_id=evidence_description_id.value,
            finding_id=finding_id,
        ),
    )

    success: bool = result["data"]["updateEvidenceDescription"]["success"]

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_update_vulnerability_commit(
    *,
    vuln_commit: str,
    vuln_id: str,
    vuln_what: str,
    vuln_where: str,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoUpdateVulnerabilityCommit(
                $vuln_commit: String!
                $vuln_id: String!
                $vuln_what: String!
                $vuln_where: String!
            ) {
                updateVulnerabilityCommit(
                    vulnerabilityCommit: $vuln_commit
                    vulnerabilityId: $vuln_id
                    vulnerabilityWhere: $vuln_what
                    vulnerabilitySpecific: $vuln_where
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoUpdateVulnerabilityCommit",
        variables=dict(
            vuln_commit=vuln_commit,
            vuln_id=vuln_id,
            vuln_what=vuln_what,
            vuln_where=vuln_where,
        ),
    )

    success: bool = (
        result["data"]["updateVulnerabilityCommit"]["success"]
        if result["data"]
        else False
    )

    if not success and "errors" not in result:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_upload_vulnerabilities(
    *,
    finding_id: str,
    stream: str,
) -> bool:
    await log(
        "debug",
        "Uploading file to finding %s with content:\n%s",
        finding_id,
        stream,
    )
    try:
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
            operation="SkimsDoUploadVulnerabilities",
            variables=dict(
                file_handle=to_in_memory_file(stream),
                finding_id=finding_id,
            ),
        )

        success: bool = result["data"]["uploadFile"]["success"]

        if not success:
            raise RetryAndFinallyReturn(success)
    except SkimsCanNotOperate:
        return False

    return success


@SHIELD
async def do_verify_request_vuln(
    *,
    closed_vulnerabilities: Tuple[str, ...],
    finding_id: str,
    justification: str,
    open_vulnerabilities: Tuple[str, ...],
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoVerifyRequestVulnerabilities(
                $finding_id: String!
                $justification: String!
                $open_vulnerabilities: [String]!
                $closed_vulnerabilities: [String]!
            ) {
                verifyVulnerabilitiesRequest(
                    closedVulnerabilities: $closed_vulnerabilities
                    findingId: $finding_id
                    justification: $justification
                    openVulnerabilities: $open_vulnerabilities
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoVerifyRequestVulnerabilities",
        variables=dict(
            closed_vulnerabilities=closed_vulnerabilities,
            finding_id=finding_id,
            justification=justification,
            open_vulnerabilities=open_vulnerabilities,
        ),
    )

    success: bool = result["data"]["verifyVulnerabilitiesRequest"]["success"]

    if not success:
        raise RetryAndFinallyReturn(success)

    return success


@SHIELD
async def do_add_execution(
    *,
    root: str,
    group_name: str,
    job_id: str,
    start_date: str,
    end_date: str,
    findings_executed: Tuple[Dict[str, Dict[str, int]], ...],
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoAddMachineExecution(
                $root: String!
                $group_name: String!
                $job_id: ID!
                $start_date: DateTime!
                $end_date: DateTime !
                $findings_executed: [String]!
            ) {
                addMachineExecution(
                    rootNickname: $root,
                    groupName: $group_name,
                    jobId: $job_id,
                    startedAt: $start_date,
                    stoppedAt: $end_date,
                    findingsExecuted: $findings_executed
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoAddMachineExecution",
        variables=dict(
            root=root,
            group_name=group_name,
            job_id=job_id,
            start_date=start_date,
            end_date=end_date,
            findings_executed=findings_executed,
        ),
    )

    success: bool = result["data"]["addMachineExecution"]["success"]

    if not success:
        raise RetryAndFinallyReturn(success)

    return success
