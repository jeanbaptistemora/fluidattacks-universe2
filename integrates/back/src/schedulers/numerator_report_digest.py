from context import (
    FI_ENVIRONMENT,
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


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

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
                        "groups": {},
                    }
                if _validate_date(toe.node.seen_at.date(), 1, 0):
                    content[toe.node.seen_first_time_by]["groups"] = {
                        group: (
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
                    }
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
                    if _validate_date(toe.node.seen_at.date(), 7, 1):
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

    if not content:
        LOGGER.info("- numerator report NOT sent")
        return


async def main() -> None:
    await send_numerator_report()
