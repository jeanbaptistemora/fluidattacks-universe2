from context import (
    FI_ENVIRONMENT,
    FI_MAIL_PRODUCTION,
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
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInputsConnection,
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
        < date_attr
        <= datetime_utils.get_now_minus_delta(days=to_day).date()
    )
    return validate_date


def _generate_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "past_day_enumerated_count": 0,
        "past_day_verified_count": 0,
        "today_enumerated_count": 0,
        "today_verified_count": 0,
        "groups": {},
    }

    return fields


def _generate_group_fields() -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "verified_count": 0,
        "enumerated_count": 0,
    }

    return fields


def _generate_count_report(
    *,
    content: Dict[str, Any],
    date_report: Optional[datetime],
    field: str,
    group: str,
    user_email: str,
) -> Dict[str, Any]:
    if user_email and date_report:
        is_valid_date = _validate_date(date_report.date(), 1, 0)

        if not content.get(user_email):
            content[user_email] = _generate_fields()

        if is_valid_date:
            if not dict(content[user_email]["groups"]).get(group):
                content[user_email]["groups"][group] = _generate_group_fields()

            content[user_email]["groups"][group][field] = (
                int(content[user_email]["groups"][group][field]) + 1
            )

            content[user_email][f"today_{field}"] = (
                int(content[user_email][f"today_{field}"]) + 1
            )
        else:
            if _validate_date(date_report.date(), 2, 1):
                content[user_email][f"past_day_{field}"] = (
                    int(content[user_email][f"past_day_{field}"]) + 1
                )

    return content


async def _generate_numerator_report(
    loaders: Dataloaders, groups_names: Tuple[str, ...]
) -> Dict[str, Any]:
    content: Dict[str, Any] = {}

    for group in groups_names:
        group_toe_inputs: ToeInputsConnection = (
            await loaders.group_toe_inputs.load(
                GroupToeInputsRequest(group_name=group)
            )
        )
        for toe in group_toe_inputs.edges:
            content = _generate_count_report(
                content=content,
                date_report=toe.node.seen_at,
                field="enumerated_count",
                group=group,
                user_email=toe.node.seen_first_time_by,
            )

            content = _generate_count_report(
                content=content,
                date_report=toe.node.attacked_at,
                field="verified_count",
                group=group,
                user_email=toe.node.attacked_by,
            )

    return content


def get_variation(num_a: int, num_b: int) -> str:
    try:
        variation: float = round((((num_b - num_a) / num_a) * 100), 2)
    except TypeError:
        return "N/A"
    except ValueError:
        return "N/A"
    except ZeroDivisionError:
        return "N/A"
    return f"{variation}%"


async def _send_mail_report(
    loaders: Any,
    content: Dict[str, Any],
    report_date: date,
    responsible: str,
) -> None:
    past_day_enumerated_count: int = int(content["past_day_enumerated_count"])
    past_day_verified_count: int = int(content["past_day_verified_count"])
    today_enumerated_count: int = int(content["today_enumerated_count"])
    today_verified_count: int = int(content["today_verified_count"])

    enumerated_variation: str = get_variation(
        past_day_enumerated_count, today_enumerated_count
    )
    verified_variation: str = get_variation(
        past_day_verified_count, today_verified_count
    )

    context: Dict[str, Any] = {
        "enumerated_variation": enumerated_variation,
        "groups": content["groups"],
        "responsible": responsible,
        "today_enumerated_count": today_enumerated_count,
        "today_verified_count": today_verified_count,
        "verified_variation": verified_variation,
    }

    await groups_mail.send_mail_numerator_report(
        loaders=loaders,
        context=context,
        email_to=[FI_MAIL_PRODUCTION],
        report_date=report_date,
    )


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)
    report_date = datetime_utils.get_now().date()

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    content: Dict[str, Any] = await _generate_numerator_report(
        loaders, groups_names
    )

    if content:
        for user_email, user_content in content.items():
            if int(user_content["today_enumerated_count"]) > 0:
                await _send_mail_report(
                    loaders, user_content, report_date, user_email
                )
    else:
        LOGGER.info("- numerator report NOT sent")
        return


async def main() -> None:
    await send_numerator_report()
