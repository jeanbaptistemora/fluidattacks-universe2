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
            if toe.node.seen_first_time_by and toe.node.seen_at:

                if not content.get(toe.node.seen_first_time_by):
                    content[toe.node.seen_first_time_by] = {
                        "weekly_count": 0,
                        "past_day_count": 0,
                        "today_count": 0,
                        "groups": {},
                    }

                if _validate_date(toe.node.seen_at.date(), 1, 0):
                    content[toe.node.seen_first_time_by]["groups"][group] = (
                        int(
                            content[toe.node.seen_first_time_by]["groups"][
                                group
                            ]
                        )
                        + 1
                        if dict(
                            content[toe.node.seen_first_time_by]["groups"]
                        ).get(group)
                        else 1
                    )
                    content[toe.node.seen_first_time_by]["today_count"] = (
                        int(
                            content[toe.node.seen_first_time_by]["today_count"]
                        )
                        + 1
                    )

                else:
                    if _validate_date(toe.node.seen_at.date(), 2, 1):
                        content[toe.node.seen_first_time_by][
                            "past_day_count"
                        ] = (
                            int(
                                content[toe.node.seen_first_time_by][
                                    "past_day_count"
                                ]
                            )
                            + 1
                        )
                    if _validate_date(toe.node.seen_at.date(), 9, 1):
                        content[toe.node.seen_first_time_by][
                            "weekly_count"
                        ] = (
                            int(
                                content[toe.node.seen_first_time_by][
                                    "weekly_count"
                                ]
                            )
                            + 1
                        )

    return content


def get_variation(num_a: int, num_b: int) -> float:
    try:
        variation: float = round((((num_b - num_a) / num_a) * 100), 2)
    except TypeError:
        return 0.0
    except ValueError:
        return 0.0
    except ZeroDivisionError:
        return 0.0
    return variation


async def _send_mail_report(
    loaders: Any,
    content: Dict[str, Any],
    report_date: date,
    responsible: str,
) -> None:
    today_count: int = int(content["today_count"])
    past_day_count: int = int(content["past_day_count"])
    weekly_count: int = int(content["weekly_count"])

    variation_from_yesterday: float = get_variation(
        past_day_count, today_count
    )
    variation_from_week: float = get_variation(weekly_count, today_count)

    context: Dict[str, Any] = {
        "groups": content["groups"],
        "responsible": responsible,
        "today_count": content["today_count"],
        "variation_yesterday": variation_from_yesterday,
        "variation_week": variation_from_week,
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
            await _send_mail_report(
                loaders, user_content, report_date, user_email
            )
    else:
        LOGGER.info("- numerator report NOT sent")
        return


async def main() -> None:
    await send_numerator_report()
