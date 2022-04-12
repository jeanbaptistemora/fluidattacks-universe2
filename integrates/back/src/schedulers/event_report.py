from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_types import (
    Event as EventType,
)
from dataloaders import (
    get_new_context,
)
from events import (
    domain as events_domain,
)
from groups import (
    domain as groups_domain,
)
import logging
from mailer import (
    events as events_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def days_to_date(date: str) -> int:
    days = (
        datetime_utils.get_now()
        - datetime_utils.get_datetime_from_iso_str(date)
    ).days
    return days


async def send_event_report() -> None:
    groups_names = await groups_domain.get_active_groups()
    loaders = get_new_context()

    if FI_ENVIRONMENT == "production":
        active_groups = await loaders.group_typed.load_many(groups_names)
        groups_names = [
            group.name
            for group in active_groups
            if group.name not in FI_TEST_PROJECTS.split(",")
        ]

    unsolved_events: List[EventType] = [
        await events_domain.get_unsolved_events(group)
        for group in groups_names
    ]

    events_filtered: List[EventType] = [
        event
        for event in unsolved_events
        if event != []
        and days_to_date(event[0]["historic_state"][-1]["date"]) in [7, 30]
    ]

    if events_filtered:
        for event in events_filtered:
            group_name = str(get_key_or_fallback(event[0], fallback=""))
            event_type = event[0]["event_type"]
            description = event[0]["detail"]
            report_date = datetime_utils.get_date_from_iso_str(
                event[0]["historic_state"][0]["date"]
            )
            await events_mail.send_mail_event_report(
                loaders=loaders,
                group_name=group_name,
                event_id=event[0]["event_id"],
                event_type=event_type,
                description=description,
                report_date=report_date,
            )
    else:
        LOGGER.info("- event report NOT sent")
        return


async def main() -> None:
    await send_event_report()
