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
) -> None:
    if user_email and date_report:
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
    loaders: Dataloaders, group: str, date_range: int, content: Dict[str, Any]
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
                )

            if draft.state.status == FindingStateStatus.REJECTED:
                _generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=datetime_utils.get_datetime_from_iso_str(
                        vuln.state.modified_date
                    ),
                    field="draft_rejected",
                    group=group,
                    user_email=vuln.state.modified_by,
                )


async def _finding_content(
    loaders: Dataloaders, group: str, date_range: int, content: Dict[str, Any]
) -> None:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(group)
    for finding in findings:
        historic_verification: Tuple[
            FindingVerification, ...
        ] = await loaders.finding_historic_verification.load(finding.id)

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
                )


async def _toe_input_content(
    loaders: Dataloaders, group: str, date_range: int, content: Dict[str, Any]
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
        )

        _generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.attacked_at,
            field="verified",
            group=group,
            user_email=toe_inputs.node.attacked_by,
        )


async def _toe_line_content(
    loaders: Dataloaders, group: str, date_range: int, content: Dict[str, Any]
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
        )


async def _generate_numerator_report(
    loaders: Dataloaders, groups_names: Tuple[str, ...]
) -> Dict[str, Any]:
    content: Dict[str, Any] = {}
    date_range = 3 if datetime_utils.get_now().weekday() == 0 else 1

    for group in groups_names:
        await collect(
            [
                _toe_input_content(loaders, group, date_range, content),
                _toe_line_content(loaders, group, date_range, content),
                _finding_content(loaders, group, date_range, content),
                _draft_content(loaders, group, date_range, content),
            ]
        )

    return content


def get_percent(num_a: int, num_b: int) -> str:
    try:
        variation: float = round(((num_a / num_b) * 100), 2)
    except TypeError:
        return "N/A"
    except ValueError:
        return "N/A"
    except ZeroDivisionError:
        return "N/A"
    return f"{variation}%"


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
    report_date = datetime_utils.get_now().date()

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group
            for group in group_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    content: Dict[str, Any] = await _generate_numerator_report(
        loaders, group_names
    )

    if content:
        for user_email, user_content in content.items():
            await _send_mail_report(
                loaders, user_content, report_date, user_email
            )
    else:
        LOGGER.info("- numerator report NOT sent")
        return


async def main() -> None:
    await send_numerator_report()
