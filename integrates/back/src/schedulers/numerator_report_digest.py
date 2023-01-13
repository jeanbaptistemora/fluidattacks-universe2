# pylint: disable=consider-using-f-string
from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_MAIL_COS,
    FI_MAIL_CTO,
    FI_TEST_ORGS,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    FindingVerification,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInputsConnection,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLinesConnection,
)
from db_model.toe_ports.types import (
    GroupToePortsRequest,
    ToePortsConnection,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from findings import (
    domain as findings_domain,
)
from group_access import (
    domain as group_access_domain,
)
import logging
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


mail_numerator_report = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(groups_mail.send_mail_numerator_report)


def _validate_date(date_attr: date, from_day: int, to_day: int) -> bool:
    validate_date: bool = (
        datetime_utils.get_now_minus_delta(days=from_day).date()
        <= date_attr
        < datetime_utils.get_now_minus_delta(days=to_day).date()
    )
    return validate_date


def _generate_count_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "count": {
            "past_day": 0,
            "today": 0,
        },
    }
    return fields


def _generate_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "enumerated_inputs": _generate_count_fields(),
        "enumerated_ports": _generate_count_fields(),
        "evidences": _generate_count_fields(),
        "verified_inputs": _generate_count_fields(),
        "verified_ports": _generate_count_fields(),
        "loc": _generate_count_fields(),
        "reattacked": _generate_count_fields(),
        "released": _generate_count_fields(),
        "draft_created": _generate_count_fields(),
        "draft_rejected": _generate_count_fields(),
        "max_cvss": 0.0,
        "oldest_draft": {"age": 0, "max_cvss": 0.0, "submit_age": 0},
        "groups": {},
    }
    return fields


def _generate_group_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "verified_inputs": 0,
        "verified_ports": 0,
        "enumerated_inputs": 0,
        "enumerated_ports": 0,
        "evidences": 0,
        "loc": 0,
        "reattacked": 0,
        "released": 0,
        "draft_created": 0,
        "draft_rejected": 0,
        "subscription": "-",
    }
    return fields


def _common_write_to_dict_today(
    *,
    content: Dict[str, Any],
    user_email: str,
    field: str,
    group: str,
    to_add: int = 1,
) -> None:
    if not dict(content[user_email]["groups"]).get(group):
        content[user_email]["groups"][group] = _generate_group_fields()

    content[user_email]["groups"][group][field] = (
        int(content[user_email]["groups"][group][field]) + to_add
    )

    content[user_email][field]["count"]["today"] = (
        int(content[user_email][field]["count"]["today"]) + to_add
    )


def _common_write_to_dict_yesterday(
    *,
    content: Dict[str, Any],
    user_email: str,
    field: str,
    to_add: int = 1,
) -> None:
    content[user_email][field]["count"]["past_day"] = (
        int(content[user_email][field]["count"]["past_day"]) + to_add
    )


def _common_generate_count_report(
    *,
    content: Dict[str, Any],
    date_range: int,
    date_report: Optional[datetime],
    field: str,
    group: str,
    to_add: int = 1,
    user_email: str,
    allowed_users: List[str],
    cvss: Decimal = Decimal("0.0"),
) -> None:
    if user_email in allowed_users and date_report:
        date_format: date = datetime_utils.as_zone(date_report).date()
        is_valid_date = _validate_date(date_format, date_range, date_range - 1)

        if not content.get(user_email):
            content[user_email] = _generate_fields()

        if is_valid_date:
            _common_write_to_dict_today(
                content=content,
                user_email=user_email,
                field=field,
                group=group,
                to_add=to_add,
            )

            if field in ["released"]:
                _max_severity_released(content, cvss, user_email)

        else:
            if datetime_utils.get_now().weekday() == 1:
                date_range = 3
            if _validate_date(date_format, date_range + 1, date_range):
                _common_write_to_dict_yesterday(
                    content=content,
                    user_email=user_email,
                    field=field,
                    to_add=to_add,
                )


async def _draft_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    group_drafts: Tuple[Finding, ...] = await loaders.group_drafts.load(group)
    for draft in group_drafts:
        cvss: Decimal = findings_domain.get_severity_score(draft.severity)
        vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(draft.id)
        for vuln in vulns:
            if draft.state.status in [
                FindingStateStatus.CREATED,
                FindingStateStatus.SUBMITTED,
            ]:
                _draft_created_content(
                    content=content,
                    cvss=cvss,
                    date_report=vuln.state.modified_date,
                    date_submission=draft.submission.modified_date
                    if draft.submission
                    else None,
                    group=group,
                    state=draft.state.status,
                    user_email=vuln.hacker_email,
                    users_email=users_email,
                )

            elif draft.state.status == FindingStateStatus.REJECTED and (
                vuln.state.reasons is None
                or (
                    vuln.state.reasons
                    and VulnerabilityStateReason.EXCLUSION
                    not in vuln.state.reasons
                )
            ):
                _common_generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=vuln.state.modified_date,
                    field="draft_rejected",
                    group=group,
                    user_email=vuln.hacker_email,
                    allowed_users=users_email,
                )

    LOGGER.info("- draft report generated in group %s", group)


def _draft_created_content(
    *,
    content: Dict[str, Any],
    cvss: Decimal = Decimal("0.0"),
    date_report: datetime,
    date_submission: Optional[datetime],
    group: str,
    state: FindingStateStatus,
    user_email: str,
    users_email: List[str],
) -> None:
    if user_email in users_email:
        if not content.get(user_email):
            content[user_email] = _generate_fields()

        _common_write_to_dict_today(
            content=content,
            user_email=user_email,
            field="draft_created",
            group=group,
        )
        _oldest_draft(
            content, cvss, date_report, date_submission, state, user_email
        )


def _oldest_draft(  # pylint: disable=too-many-arguments
    content: Dict[str, Any],
    cvss: Decimal,
    date_report: datetime,
    date_submission: Optional[datetime],
    state: FindingStateStatus,
    user_email: str,
) -> None:
    if not content.get(user_email):
        content[user_email] = _generate_fields()

    draft_days = (datetime_utils.get_now().date() - date_report.date()).days

    if date_submission:
        submission_days = (
            datetime_utils.get_now().date() - date_submission.date()
        ).days

        if (
            content[user_email]["oldest_draft"]["submit_age"]
            <= submission_days
            and state == FindingStateStatus.SUBMITTED
        ):
            if content[user_email]["oldest_draft"]["max_cvss"] < cvss:
                content[user_email]["oldest_draft"]["max_cvss"] = cvss
            content[user_email]["oldest_draft"]["submit_age"] = submission_days
    else:
        if content[user_email]["oldest_draft"]["age"] <= draft_days:
            if content[user_email]["oldest_draft"]["max_cvss"] < cvss:
                content[user_email]["oldest_draft"]["max_cvss"] = cvss
            content[user_email]["oldest_draft"]["age"] = draft_days


async def _finding_reattacked(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    historic_verification: Tuple[
        FindingVerification, ...
    ] = await loaders.finding_historic_verification.load(finding_id)

    for verification in historic_verification:
        if (
            verification.vulnerability_ids
            and verification.status == FindingVerificationStatus.VERIFIED
        ):
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=verification.modified_date,
                field="reattacked",
                group=group,
                to_add=len(verification.vulnerability_ids),
                user_email=verification.modified_by,
                allowed_users=users_email,
            )


async def _finding_vulns_released(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding: Finding,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:

    if finding.state.status != FindingStateStatus.APPROVED:
        return None

    cvss: Decimal = findings_domain.get_severity_score(finding.severity)
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load(finding.id)
    historic_state_loader = loaders.vulnerability_historic_state

    for vuln in vulnerabilities:
        historic_state_loader.clear(vuln.id)
        historic_state: Tuple[
            VulnerabilityState, ...
        ] = await historic_state_loader.load(vuln.id)
        for state in historic_state:
            if state.status == VulnerabilityStateStatus.VULNERABLE:
                _common_generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=state.modified_date,
                    field="released",
                    group=group,
                    user_email=state.modified_by,
                    allowed_users=users_email,
                    cvss=cvss,
                )
                evidences = len(
                    [
                        evidence_id
                        for evidence_id in finding.evidences._fields
                        if getattr(finding.evidences, evidence_id) is not None
                    ]
                )
                _common_generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=state.modified_date,
                    field="evidences",
                    group=group,
                    user_email=state.modified_by,
                    allowed_users=users_email,
                    to_add=evidences,
                )


def _max_severity_released(
    content: Dict[str, Any],
    cvss: Decimal,
    user_email: str,
) -> None:
    if content[user_email]["max_cvss"] < cvss:
        content[user_email]["max_cvss"] = cvss


async def _finding_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(group)

    for finding in findings:
        await collect(
            [
                _finding_reattacked(
                    loaders,
                    finding.id,
                    group,
                    date_range,
                    content,
                    users_email,
                ),
                _finding_vulns_released(
                    loaders, finding, group, date_range, content, users_email
                ),
            ]
        )

    LOGGER.info("- finding report generated in group %s", group)


async def _toe_input_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    group_toe_inputs: ToeInputsConnection = (
        await loaders.group_toe_inputs.load(
            GroupToeInputsRequest(group_name=group)
        )
    )
    for toe_inputs in group_toe_inputs.edges:
        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.state.seen_at,
            field="enumerated_inputs",
            group=group,
            user_email=toe_inputs.node.state.seen_first_time_by,
            allowed_users=users_email,
        )

        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.state.attacked_at,
            field="verified_inputs",
            group=group,
            user_email=toe_inputs.node.state.attacked_by,
            allowed_users=users_email,
        )

    LOGGER.info("- toe input report generated in group %s", group)


async def _toe_line_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    group_toe_lines: ToeLinesConnection = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(group_name=group)
    )
    for toe_lines in group_toe_lines.edges:
        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_lines.node.state.attacked_at,
            field="loc",
            group=group,
            user_email=toe_lines.node.state.attacked_by,
            to_add=toe_lines.node.state.attacked_lines,
            allowed_users=users_email,
        )

    LOGGER.info("- toe lines report generated in group %s", group)


async def _toe_port_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: Dict[str, Any],
    users_email: List[str],
) -> None:
    group_toe_ports: ToePortsConnection = await loaders.group_toe_ports.load(
        GroupToePortsRequest(group_name=group)
    )
    for toe_inputs in group_toe_ports.edges:
        if toe_inputs.node.seen_first_time_by:
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_inputs.node.seen_at,
                field="enumerated_ports",
                group=group,
                user_email=toe_inputs.node.seen_first_time_by,
                allowed_users=users_email,
            )

        if toe_inputs.node.state.attacked_by:
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_inputs.node.state.attacked_at,
                field="verified_ports",
                group=group,
                user_email=toe_inputs.node.state.attacked_by,
                allowed_users=users_email,
            )

    LOGGER.info("- toe port report generated in group %s", group)


async def _generate_numerator_report(
    loaders: Dataloaders, groups_names: Tuple[str, ...], date_range: int
) -> Dict[str, Any]:
    content: Dict[str, Any] = {}
    allowed_roles: set[str] = {
        "architect",
        "hacker",
        "reattacker",
        "resourcer",
        "reviewer",
    }

    for group in groups_names:
        users_email: list[
            str
        ] = await group_access_domain.get_stakeholders_email_by_roles(
            loaders=loaders,
            group_name=group,
            roles=allowed_roles,
        )
        await collect(
            [
                _toe_input_content(
                    loaders, group, date_range, content, users_email
                ),
                _toe_line_content(
                    loaders, group, date_range, content, users_email
                ),
                _toe_port_content(
                    loaders, group, date_range, content, users_email
                ),
                _finding_content(
                    loaders, group, date_range, content, users_email
                ),
                _draft_content(
                    loaders, group, date_range, content, users_email
                ),
            ]
        )

    for data in content.values():
        for group_name in data["groups"]:
            group_data: Group = await loaders.group.load(group_name)
            data["groups"][group_name]["subscription"] = (
                "o" if group_data.state.type == "ONESHOT" else "c"
            )

    LOGGER.info("- general report successfully generated")

    return content


def get_percent(num_a: int, num_b: int) -> str:
    try:
        variation: float = num_a / num_b
    except TypeError:
        return "-"
    except ValueError:
        return "-"
    except ZeroDivisionError:
        return "-"
    return "{:+.0%}".format(variation)


def _generate_count_and_variation(content: Dict[str, Any]) -> Dict[str, Any]:
    count_and_variation: Dict[str, Any] = {
        key: {
            "count": (count := value["count"])["today"],
            "variation": get_percent(
                count["today"] - count["past_day"],
                count["past_day"],
            ),
        }
        for key, value in content.items()
    }
    count_and_variation["effectiveness"] = get_percent(
        content["released"]["count"]["today"]
        - content["draft_rejected"]["count"]["today"],
        content["released"]["count"]["today"],
    )

    return count_and_variation


async def _send_mail_report(
    loaders: Dataloaders,
    content: Dict[str, Any],
    report_date: date,
    responsible: str,
) -> None:
    groups_content = content.pop("groups")
    max_cvss = content.pop("max_cvss")
    oldest_draft = content.pop("oldest_draft")
    count_var_report: Dict[str, Any] = _generate_count_and_variation(content)

    context: Dict[str, Any] = {
        "count_var_report": count_var_report,
        "groups": groups_content,
        "max_cvss": max_cvss,
        "oldest_draft": oldest_draft,
        "responsible": responsible,
    }

    await mail_numerator_report(
        loaders=loaders,
        context=context,
        email_to=[responsible],
        email_cc=[FI_MAIL_COS, FI_MAIL_CTO],
        report_date=report_date,
    )


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    test_group_names = tuple(FI_TEST_PROJECTS.split(","))

    async for _, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        for group_name in org_groups_names:
            if (
                org_name in FI_TEST_ORGS.lower().split(",")
            ) and group_name not in test_group_names:
                test_group_names += tuple(org_groups_names)
    date_range = 3 if datetime_utils.get_now().weekday() == 0 else 1
    report_date = datetime_utils.get_now_minus_delta(days=date_range).date()

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group for group in group_names if group not in test_group_names
        )

    content: Dict[str, Any] = await _generate_numerator_report(
        loaders, group_names, date_range
    )

    if content:
        for user_email, user_content in content.items():
            try:
                await _send_mail_report(
                    loaders, user_content, report_date, user_email
                )
            except KeyError:
                LOGGER.info(
                    "- key error, email not sent",
                    extra={"extra": {"email": user_email}},
                )
                continue
    else:
        LOGGER.info("- numerator report NOT sent")


async def main() -> None:
    await send_numerator_report()
