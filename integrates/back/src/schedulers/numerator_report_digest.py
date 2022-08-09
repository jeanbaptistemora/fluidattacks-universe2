# pylint: disable=consider-using-f-string
from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_MAIL_COS,
    FI_MAIL_CTO,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
from db_model.enums import (
    StateRemovalJustification,
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from group_access import (
    domain as group_access_domain,
)
import logging
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
        "enumerated": _generate_count_fields(),
        "verified": _generate_count_fields(),
        "loc": _generate_count_fields(),
        "reattacked": _generate_count_fields(),
        "released": _generate_count_fields(),
        "draft_created": _generate_count_fields(),
        "draft_rejected": _generate_count_fields(),
        "groups": {},
    }
    return fields


def _generate_group_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "verified": 0,
        "enumerated": 0,
        "loc": 0,
        "reattacked": 0,
        "released": 0,
        "draft_created": 0,
        "draft_rejected": 0,
    }
    return fields


def _generate_count_report(
    *,
    content: Dict[str, Any],
    date_range: int,
    date_report: Optional[datetime],
    field: str,
    group: str,
    to_add: int = 1,
    user_email: str,
    allowed_users: List[str],
) -> None:
    if user_email and user_email in allowed_users and date_report:
        date_format: date = datetime_utils.as_zone(date_report).date()
        is_valid_date = _validate_date(date_format, date_range, date_range - 1)

        if not content.get(user_email):
            content[user_email] = _generate_fields()

        if is_valid_date:
            if not dict(content[user_email]["groups"]).get(group):
                content[user_email]["groups"][group] = _generate_group_fields()

            content[user_email]["groups"][group][field] = (
                int(content[user_email]["groups"][group][field]) + to_add
            )

            content[user_email][field]["count"]["today"] = (
                int(content[user_email][field]["count"]["today"]) + to_add
            )
        else:
            if datetime_utils.get_now().weekday() == 1:
                date_range = 3
            if _validate_date(date_format, date_range + 1, date_range):
                content[user_email][field]["count"]["past_day"] = (
                    int(content[user_email][field]["count"]["past_day"])
                    + to_add
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
        vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(draft.id)
        for vuln in vulns:
            if draft.state.status in [
                FindingStateStatus.CREATED,
                FindingStateStatus.SUBMITTED,
            ]:
                _generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=datetime_utils.get_datetime_from_iso_str(
                        vuln.state.modified_date
                    ),
                    field="draft_created",
                    group=group,
                    user_email=vuln.state.modified_by,
                    allowed_users=users_email,
                )

            if (
                draft.state.status == FindingStateStatus.REJECTED
                and vuln.state.justification
                != StateRemovalJustification.EXCLUSION
            ):
                _generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=datetime_utils.get_datetime_from_iso_str(
                        vuln.state.modified_date
                    ),
                    field="draft_rejected",
                    group=group,
                    user_email=vuln.state.modified_by,
                    allowed_users=users_email,
                )

    LOGGER.info("- draft report generated in group %s", group)


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
            _generate_count_report(
                content=content,
                date_range=date_range,
                date_report=datetime_utils.get_datetime_from_iso_str(
                    verification.modified_date
                ),
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

    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load(finding.id)

    for vuln in vulnerabilities:
        _generate_count_report(
            content=content,
            date_range=date_range,
            date_report=datetime_utils.get_datetime_from_iso_str(
                finding.state.modified_date
            ),
            field="released",
            group=group,
            user_email=vuln.hacker_email,
            allowed_users=users_email,
        )


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
        _generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.seen_at,
            field="enumerated",
            group=group,
            user_email=toe_inputs.node.seen_first_time_by,
            allowed_users=users_email,
        )

        _generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.attacked_at,
            field="verified",
            group=group,
            user_email=toe_inputs.node.attacked_by,
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
        _generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_lines.node.attacked_at,
            field="loc",
            group=group,
            user_email=toe_lines.node.attacked_by,
            to_add=toe_lines.node.attacked_lines,
            allowed_users=users_email,
        )

    LOGGER.info("- toe lines report generated in group %s", group)


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
                _finding_content(
                    loaders, group, date_range, content, users_email
                ),
                _draft_content(
                    loaders, group, date_range, content, users_email
                ),
            ]
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
    count_and_variation: Dict[str, Any] = {}
    for key, value in content.items():
        if key not in ["groups"]:
            count_and_variation[key] = {
                "count": value["count"]["today"],
                "variation": get_percent(
                    value["count"]["today"] - value["count"]["past_day"],
                    value["count"]["past_day"],
                ),
            }
    count_and_variation["effectiveness"] = get_percent(
        content["released"]["count"]["today"]
        - content["draft_rejected"]["count"]["today"],
        content["released"]["count"]["today"],
    )

    return count_and_variation


async def _send_mail_report(
    loaders: Any,
    content: Dict[str, Any],
    report_date: date,
    responsible: str,
) -> None:
    count_var_report: Dict[str, Any] = _generate_count_and_variation(content)

    context: Dict[str, Any] = {
        "count_var_report": count_var_report,
        "groups": content["groups"],
        "responsible": responsible,
    }

    await groups_mail.send_mail_numerator_report(
        loaders=loaders,
        context=context,
        email_to=[responsible],
        email_cc=[FI_MAIL_COS, FI_MAIL_CTO],
        report_date=report_date,
    )


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups: Tuple[Group, ...] = await orgs_domain.get_all_active_groups(
        loaders
    )
    group_names = tuple(
        group.name for group in groups if group.state.has_squad
    )
    date_range = 3 if datetime_utils.get_now().weekday() == 0 else 1
    report_date = datetime_utils.get_now_minus_delta(days=date_range).date()

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group
            for group in group_names
            if group not in FI_TEST_PROJECTS.split(",")
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
        return


async def main() -> None:
    await send_numerator_report()
