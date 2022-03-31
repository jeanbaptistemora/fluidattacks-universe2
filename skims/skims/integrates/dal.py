# pylint: disable=too-many-lines
from aiogqlc import (
    GraphQLClient,
)
import aiohttp
from aiohttp.client_reqrep import (
    ClientResponse,
)
import asyncio
from contextlib import (
    suppress,
)
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
    Union,
)
from utils.function import (
    shield,
    SkimsCanNotOperate,
    StopRetrying,
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


async def _request(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
    client: Optional[GraphQLClient] = None,
) -> ClientResponse:
    if client and not client.session.closed:
        response: aiohttp.ClientResponse = await client.execute(
            query=query,
            operation=operation,
            variables=variables,
        )
    else:
        async with graphql_client() as client:
            response = await client.execute(
                query=query,
                operation=operation,
                variables=variables,
            )
    return response


# @rate_limited(rpm=DEFAULT_RATE_LIMIT)
async def _execute(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
    client: Optional[GraphQLClient] = None,
) -> Dict[str, Any]:
    while True:
        response = await _request(
            query=query,
            operation=operation,
            variables=variables,
            client=client,
        )
        if response.status == 429 and (
            seconds := response.headers.get("retry-after")
        ):
            await asyncio.sleep(int(seconds) + 1)
        else:
            break

    if response.status >= 400:
        await log("debug", "query: %s", query)
        await log("debug", "variables: %s", variables)
        await log("debug", "response status: %s", response.status)
        raise aiohttp.ClientResponseError(
            response.request_info,
            (response,),
            status=response.status,
            headers=response.headers,
            message=f"query: {query}\nvariables: {variables}",
        )

    result: Dict[str, Any] = (await response.json()) or {}

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
    client: Optional[GraphQLClient] = None,
) -> Optional[str]:
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        role: str = result["data"]["group"]["userRole"]
        return role

    return None


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
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        opt_findings = result["data"]["group"]["findings"]
    with suppress(AttributeError, KeyError, TypeError):
        opt_drafts = result["data"]["group"]["drafts"]

    _findings = opt_findings if opt_findings is not None else []
    _drafts = opt_drafts if opt_drafts is not None else []

    findings: List[ResultGetGroupFindings] = [
        ResultGetGroupFindings(
            identifier=finding["id"],
            title=finding["title"],
        )
        for finding in (_findings + _drafts)
    ]

    findings = sorted(
        findings,
        key=lambda result: (result.title, result.identifier),
    )

    return tuple(findings)


@SHIELD
async def get_group_language(
    group: str,
    client: Optional[GraphQLClient] = None,
) -> Optional[core_model.LocalesEnum]:
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return core_model.LocalesEnum(result["data"]["group"]["language"])

    return None


@SHIELD
async def get_group_open_severity(
    group: str,
    client: Optional[GraphQLClient] = None,
) -> Optional[float]:
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return sum(
            finding["openVulnerabilities"]
            * (4 ** (finding["severityScore"] - 4))
            for finding in result["data"]["group"]["findings"]
        )

    return None


class ResultGetGroupRoots(NamedTuple):
    id: str
    environment_urls: List[str]
    nickname: str
    gitignore: List[str]
    download_url: Optional[str] = None


@SHIELD
async def get_group_roots(
    *,
    group: str,
    client: Optional[GraphQLClient] = None,
) -> Optional[Tuple[ResultGetGroupRoots, ...]]:
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
                            url
                            id
                            gitignore
                        }
                    }
                }
            }
        """,
        operation="SkimsGetGroupRoots",
        variables=dict(
            group=group,
        ),
        client=client,
    )

    try:
        return tuple(
            ResultGetGroupRoots(
                environment_urls=root["environmentUrls"],
                nickname=root["nickname"],
                gitignore=root["gitignore"],
                id=root["id"],
            )
            for root in result["data"]["group"]["roots"]
        )
    except (AttributeError, KeyError, TypeError):
        return None


@SHIELD
async def get_group_root_download_url(
    *,
    group: str,
    root_id: str,
    client: Optional[GraphQLClient] = None,
) -> Tuple[str, Optional[str]]:
    result = await _execute(
        query="""
            query SkimsGetGroupRootDownloadUrl(
                $groupName: String!, $rootId: ID!
            ) {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  downloadUrl
                }
              }
            }
        """,
        operation="SkimsGetGroupRootDownloadUrl",
        variables={"groupName": group, "rootId": root_id},
        client=client,
    )

    try:
        return (root_id, result["data"]["root"]["downloadUrl"])

    except (AttributeError, KeyError, TypeError):
        return (root_id, None)


@SHIELD
async def get_finding_current_release_status(
    *,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )
    with suppress(AttributeError, KeyError, TypeError):
        return core_model.FindingReleaseStatusEnum(
            result["data"]["finding"]["currentState"]
        )
    return core_model.FindingReleaseStatusEnum.APPROVED


@SHIELD
async def get_finding_vulnerabilities(
    *,
    finding: core_model.FindingEnum,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
                        id
                        lastVerificationDate
                        source
                        specific
                        stream
                        verification
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
        client=client,
    )

    store: EphemeralStore = get_ephemeral_store()
    vulnerabilities = []
    with suppress(AttributeError, KeyError, TypeError):
        vulnerabilities = result["data"]["finding"]["vulnerabilities"]
    for vulnerability in vulnerabilities:
        kind = core_model.VulnerabilityKindEnum(
            vulnerability["vulnerabilityType"]
        )
        namespace, what = core_model.Vulnerability.what_from_integrates(
            kind=kind,
            what_on_integrates=vulnerability["where"],
        )
        source = (
            core_model.VulnerabilitySourceEnum.SKIMS
            if vulnerability["source"] in {"machine", "skims"}
            else core_model.VulnerabilitySourceEnum.INTEGRATES
        )
        verification = (
            core_model.VulnerabilityVerification(
                date=vulnerability["lastVerificationDate"],
                state=core_model.VulnerabilityVerificationStateEnum(
                    str(vulnerability["verification"]).upper()
                ),
            )
            if vulnerability["lastVerificationDate"] is not None
            and vulnerability["verification"] is not None
            else None
        )
        stream = vulnerability["stream"]
        if stream is not None:
            stream = stream.replace(" > ", ",")

        store.store(
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
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )

    with suppress(ArithmeticError):
        return result["data"]["addGitRoot"]["success"]
    return False


class ResultCreateDraft(NamedTuple):
    success: bool
    id: str = ""


@SHIELD
async def do_create_draft(
    *,
    finding: core_model.FindingEnum,
    group: str,
    client: Optional[GraphQLClient] = None,
) -> ResultCreateDraft:
    try:
        result = await _execute(
            query="""
            mutation SkimsDoAddDraft(
                $impact: String
                $description: String
                $group: String!
                $recommendation: String
                $requirements: String
                $threat: String
                $title: String!
            ) {
                addDraft(
                    attackVectorDescription: $impact
                    description: $description
                    groupName: $group
                    recommendation: $recommendation
                    requirements: $requirements
                    threat: $threat
                    title: $title
                ) {
                    draftId
                    success
                }
            }
        """,
            operation="SkimsDoAddDraft",
            variables=dict(
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
            client=client,
        )
        with suppress(AttributeError, KeyError, TypeError):
            return ResultCreateDraft(
                id=result["data"]["addDraft"]["draftId"],
                success=result["data"]["addDraft"]["success"],
            )

    except SkimsCanNotOperate:
        return ResultCreateDraft(success=False)

    return ResultCreateDraft(success=False)


@SHIELD
async def do_delete_finding(
    *,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )
    success: bool = False
    with suppress(AttributeError, KeyError, TypeError):
        success = result["data"]["removeFinding"]["success"]

    await log("warn", "Removing finding: %s, success: %s", finding_id, success)

    return success


@SHIELD
async def do_approve_draft(
    *,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
            client=client,
        )

        with suppress(AttributeError, KeyError, TypeError):
            return result["data"]["approveDraft"]["success"]

    except SkimsCanNotOperate:
        return False

    return False


@SHIELD
async def do_submit_draft(
    *,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
            client=client,
        )

        with suppress(AttributeError, KeyError, TypeError):
            return result["data"]["submitDraft"]["success"]

    except SkimsCanNotOperate:
        return False

    return False


@SHIELD
async def do_update_finding_severity(
    *,
    finding_id: str,
    severity: Dict[str, float],
    client: Optional[GraphQLClient] = None,
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
            client=client,
        )

        with suppress(AttributeError, KeyError, TypeError):
            return result["data"]["updateSeverity"]["success"]
    except SkimsCanNotOperate:
        return False
    return False


# @rate_limited(rpm=DO_UPDATE_EVIDENCE_RATE_LIMIT)
@SHIELD
async def do_update_evidence(
    *,
    evidence_id: core_model.FindingEvidenceIDEnum,
    evidence_stream: bytes,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["updateEvidence"]["success"]

    return False


@SHIELD
async def do_update_evidence_description(
    *,
    evidence_description: str,
    evidence_description_id: core_model.FindingEvidenceDescriptionIDEnum,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["updateEvidenceDescription"]["success"]

    return False


async def do_update_vulnerability_commit(
    *,
    vuln_commit: str,
    vuln_id: str,
    vuln_what: str,
    vuln_where: str,
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )
    if "errors" in result:
        return False

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["updateVulnerabilityCommit"]["success"]

    return False


@SHIELD
async def do_upload_vulnerabilities(
    *,
    finding_id: str,
    stream: str,
    client: Optional[GraphQLClient] = None,
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
            client=client,
        )

        with suppress(AttributeError, KeyError, TypeError):
            return result["data"]["uploadFile"]["success"]

    except SkimsCanNotOperate:
        return False

    return False


@SHIELD
async def do_verify_request_vuln(
    *,
    closed_vulnerabilities: Tuple[str, ...],
    finding_id: str,
    justification: str,
    open_vulnerabilities: Tuple[str, ...],
    client: Optional[GraphQLClient] = None,
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
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["verifyVulnerabilitiesRequest"]["success"]
    return False


@SHIELD
async def do_add_execution(
    *,
    root: str,
    group_name: str,
    job_id: str,
    start_date: str,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
    commit_hash: str,
    client: Optional[GraphQLClient] = None,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoAddMachineExecution(
                $root: String!
                $group_name: String!
                $job_id: ID!
                $start_date: DateTime!
                $findings_executed: [MachineFindingResultInput]
                $commit_hash: String!
            ) {
                addMachineExecution(
                    rootNickname: $root,
                    groupName: $group_name,
                    jobId: $job_id,
                    startedAt: $start_date,
                    findingsExecuted: $findings_executed
                    gitCommit: $commit_hash
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
            findings_executed=findings_executed,
            commit_hash=commit_hash,
        ),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["addMachineExecution"]["success"]

    return False


@SHIELD
async def do_finish_execution(
    *,
    root: str,
    group_name: str,
    job_id: str,
    end_date: str,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
    client: Optional[GraphQLClient] = None,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoFinishMachineExecution(
                $root: String!
                $group_name: String!
                $job_id: ID!
                $end_date: DateTime!
                $findings_executed: [MachineFindingResultInput]
            ) {
                finishMachineExecution(
                    rootNickname: $root,
                    groupName: $group_name,
                    jobId: $job_id,
                    stoppedAt: $end_date,
                    findingsExecuted: $findings_executed
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoFinishMachineExecution",
        variables=dict(
            root=root,
            group_name=group_name,
            job_id=job_id,
            end_date=end_date,
            findings_executed=findings_executed,
        ),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["addMachineExecution"]["success"]

    return False


@SHIELD
async def do_add_finding_consult(
    *,
    content: str,
    finding_id: str,
    parent: str,
    comment_type: str,
    client: Optional[GraphQLClient] = None,
) -> bool:

    result = await _execute(
        query="""
            mutation SkimsAddFindingConsult(
                $content: String!
                $finding_id: String!
                $parent: GenericScalar!
                $comment_type: FindingConsultType!
            ) {
                addFindingConsult(
                    content: $content
                    findingId: $finding_id
                    parentComment: $parent
                    type: $comment_type
                ) {
                    commentId
                    success
                }
            }
        """,
        operation="SkimsAddFindingConsult",
        variables=dict(
            content=content,
            finding_id=finding_id,
            parent=parent,
            comment_type=comment_type,
        ),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["addFindingConsult"]["success"]

    return False


@SHIELD
async def get_finding_consult(
    *,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
) -> str:
    result = await _execute(
        query="""
            query SkimsGetFindingConsult(
                $finding_id: String!
            ) {
                finding(identifier: $finding_id) {
                    consulting {
                        content
                    }
                }
            }
        """,
        operation="SkimsGetFindingConsult",
        variables=dict(
            finding_id=finding_id,
        ),
        client=client,
    )
    with suppress(AttributeError, KeyError, TypeError):
        solution: str = result["data"]["finding"]["consulting"]

    return solution
