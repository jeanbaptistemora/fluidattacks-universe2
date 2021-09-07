from aioextensions import (
    collect,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    InvalidDraftTitle,
    NotSubmitted,
)
from custom_types import (
    Finding as FindingType,
    User as UserType,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from decimal import (
    Decimal,
)
from findings import (
    dal as findings_dal,
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    token as token_utils,
    vulnerabilities as vulns_utils,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)
import uuid
from vulnerabilities import (
    domain as vulns_domain,
)


async def approve_draft(
    context: Any, draft_id: str, reviewer_email: str
) -> Tuple[bool, str]:
    finding_all_vulns_loader = context.loaders.finding_vulns_all
    finding_vulns_loader = context.loaders.finding_vulns_nzr
    finding_loader = context.loaders.finding
    draft_data = await finding_loader.load(draft_id)
    release_date: str = ""
    success = False

    if not findings_utils.is_approved(
        draft_data
    ) and not findings_utils.is_deleted(draft_data):
        vulns = await finding_vulns_loader.load(draft_id)
        has_vulns = [
            vuln for vuln in vulns if vulns_utils.filter_deleted_status(vuln)
        ]
        if has_vulns:
            if findings_utils.is_submitted(draft_data):
                release_date = datetime_utils.get_now_as_str()
                history = cast(
                    List[Dict[str, str]], draft_data["historic_state"]
                )
                history.append(
                    {
                        "date": release_date,
                        "analyst": reviewer_email,
                        "source": requests_utils.get_source(context),
                        "state": "APPROVED",
                    }
                )
                finding_update_success = await findings_dal.update(
                    draft_id, {"historic_state": history}
                )
                all_vulns = await finding_all_vulns_loader.load(draft_id)
                vuln_update_success = await collect(
                    vulns_domain.update_historics_dates(
                        draft_id, vuln, release_date
                    )
                    for vuln in all_vulns
                )
                success = all(vuln_update_success) and finding_update_success
            else:
                raise NotSubmitted()
        else:
            raise DraftWithoutVulns()
    else:
        raise AlreadyApproved()
    return success, release_date


async def approve_draft_new(
    context: Any,
    finding_id: str,
    user_email: str,
) -> str:
    finding_all_vulns_loader = context.loaders.finding_vulns_all
    finding_nzr_vulns_loader = context.loaders.finding_vulns_nzr
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    nzr_vulns = await finding_nzr_vulns_loader.load(finding_id)
    has_vulns = bool(
        [vuln for vuln in nzr_vulns if vulns_utils.filter_deleted_status(vuln)]
    )
    if not has_vulns:
        raise DraftWithoutVulns()

    approval_date = datetime_utils.get_iso_date()
    new_state = FindingState(
        modified_by=user_email,
        modified_date=approval_date,
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.APPROVED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    all_vulns = await finding_all_vulns_loader.load(finding_id)
    old_format_approval_date = datetime_utils.get_as_str(
        datetime.fromisoformat(approval_date)
    )
    await collect(
        vulns_domain.update_historics_dates(
            finding_id, vuln, old_format_approval_date
        )
        for vuln in all_vulns
    )
    return approval_date


async def add_draft(
    info: GraphQLResolveInfo, group_name: str, title: str, **kwargs: Any
) -> bool:
    finding_id = str(uuid.uuid4())
    group_name = group_name.lower()
    creation_date = datetime_utils.get_now_as_str()
    user_data = cast(UserType, await token_utils.get_jwt_content(info.context))
    analyst_email = str(user_data.get("user_email", ""))
    source = requests_utils.get_source(info.context)
    submission_history = {
        "analyst": analyst_email,
        "date": creation_date,
        "source": source,
        "state": "CREATED",
    }

    if "description" in kwargs:
        kwargs["vulnerability"] = kwargs.pop("description")
    if "recommendation" in kwargs:
        kwargs["effect_solution"] = kwargs.pop("recommendation")
    if "type" in kwargs:
        kwargs["finding_type"] = kwargs.pop("type")

    finding_attrs = kwargs.copy()
    finding_attrs.update(
        {
            "analyst": analyst_email,
            "cvss_version": "3.1",
            "exploitability": 0,
            "files": [],
            "finding": title,
            "historic_state": [submission_history],
        }
    )

    if findings_utils.is_valid_finding_title(title):
        return await findings_dal.add(finding_id, group_name, finding_attrs)
    raise InvalidDraftTitle()


async def add_draft_new(
    context: Any,
    group_name: str,
    user_email: str,
    draft_info: FindingDraftToAdd,
) -> None:
    if not findings_utils.is_valid_finding_title(draft_info.title):
        raise InvalidDraftTitle()

    group_name = group_name.lower()
    finding_id = str(uuid.uuid4())
    draft = Finding(
        affected_systems=draft_info.affected_systems,
        analyst_email=user_email,
        attack_vector_description=draft_info.attack_vector_description,
        description=draft_info.description,
        group_name=group_name,
        id=finding_id,
        state=FindingState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            source=requests_utils.get_source_new(context),
            status=FindingStateStatus.CREATED,
        ),
        risk=draft_info.risk,
        recommendation=draft_info.recommendation,
        requirements=draft_info.requirements,
        title=draft_info.title,
        threat=draft_info.threat,
        type=draft_info.type,
    )
    await findings_model.add(finding=draft)


async def get_drafts_by_group(
    group_name: str,
    attrs: Optional[Set[str]] = None,
    include_deleted: bool = False,
) -> List[Dict[str, FindingType]]:
    if attrs and "historic_state" not in attrs:
        attrs.add("historic_state")
    findings = await findings_dal.get_findings_by_group(group_name, attrs)
    findings = findings_utils.filter_non_approved_findings(findings)
    if not include_deleted:
        findings = findings_utils.filter_non_deleted_findings(findings)
    return [
        findings_utils.format_finding(finding, attrs) for finding in findings
    ]


async def list_drafts(
    group_names: List[str], include_deleted: bool = False
) -> List[List[str]]:
    """Returns a list the list of finding ids associated with the groups"""
    attrs = {"finding_id", "historic_state"}
    findings = await collect(
        get_drafts_by_group(group_name, attrs, include_deleted)
        for group_name in group_names
    )
    findings = [
        list(map(lambda finding: finding["finding_id"], group_findings))
        for group_findings in findings
    ]
    return cast(List[List[str]], findings)


async def reject_draft(
    context: Any, draft_id: str, reviewer_email: str
) -> bool:
    finding_loader = context.loaders.finding
    draft_data = await finding_loader.load(draft_id)
    history = cast(List[Dict[str, str]], draft_data["historic_state"])
    success = False
    is_finding_approved = findings_utils.is_approved(draft_data)
    is_finding_deleted = findings_utils.is_deleted(draft_data)
    is_finding_submitted = findings_utils.is_submitted(draft_data)

    if not is_finding_approved and not is_finding_deleted:
        if is_finding_submitted:
            rejection_date = datetime_utils.get_now_as_str()
            source = requests_utils.get_source(context)
            history.append(
                {
                    "date": rejection_date,
                    "analyst": reviewer_email,
                    "source": source,
                    "state": "REJECTED",
                }
            )
            success = await findings_dal.update(
                draft_id, {"historic_state": history}
            )
        else:
            raise NotSubmitted()
    else:
        raise AlreadyApproved()
    return success


async def reject_draft_new(
    context: Any, finding_id: str, user_email: str
) -> None:
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.REJECTED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )


async def submit_draft(  # pylint: disable=too-many-locals
    context: Any, finding_id: str, analyst_email: str
) -> bool:
    success = False
    finding_vulns_loader = context.loaders.finding_vulns
    finding_loader = context.loaders.finding
    finding = await finding_loader.load(finding_id)
    is_finding_approved = findings_utils.is_approved(finding)
    is_finding_deleted = findings_utils.is_deleted(finding)
    is_finding_submitted = findings_utils.is_submitted(finding)

    if not is_finding_approved and not is_finding_deleted:
        if not is_finding_submitted:
            has_severity = float(str(finding["severity_score"])) > Decimal(0)
            has_vulns = await finding_vulns_loader.load(finding_id)

            if all([has_severity, has_vulns]):
                report_date = datetime_utils.get_now_as_str()
                source = requests_utils.get_source(context)
                history = cast(List[Dict[str, str]], finding["historic_state"])
                history.append(
                    {
                        "analyst": analyst_email,
                        "date": report_date,
                        "source": source,
                        "state": "SUBMITTED",
                    }
                )
                success = await findings_dal.update(
                    finding_id, {"historic_state": history}
                )
            else:
                required_fields = {
                    # 'evidence': has_evidence,
                    "severity": has_severity,
                    "vulnerabilities": has_vulns,
                }
                raise IncompleteDraft(
                    [
                        field
                        for field in required_fields
                        if not required_fields[field]
                    ]
                )
        else:
            raise AlreadySubmitted()
    else:
        raise AlreadyApproved()
    return success


async def submit_draft_new(
    context: Any, finding_id: str, user_email: str
) -> None:
    finding_vulns_loader = context.loaders.finding_vulns
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status == FindingStateStatus.SUBMITTED:
        raise AlreadySubmitted()

    has_severity = findings_domain.get_severity_score_new(
        finding.severity
    ) > Decimal(0)
    has_vulns = bool(await finding_vulns_loader.load(finding_id))
    if not has_severity or not has_vulns:
        required_fields = {
            "severity": has_severity,
            "vulnerabilities": has_vulns,
        }
        raise IncompleteDraft(
            [field for field in required_fields if not required_fields[field]]
        )

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.SUBMITTED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
