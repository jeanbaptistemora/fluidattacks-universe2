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
from datetime import (
    date as date_type,
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
        groups_names = [
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        ]

    unsolved_events = [
        event
        for group in groups_names
        for event in await events_domain.get_unsolved_events(group)
    ]

    events_filtered: List[EventType] = [
        event
        for event in unsolved_events
        if days_to_date(event["historic_state"][-1]["date"]) in [7, 30]
    ]

    if events_filtered:
        for event in events_filtered:
            group_name = str(get_key_or_fallback(event, fallback=""))
            event_type = event["event_type"]
            description = event["detail"]
            report_date: date_type = datetime_utils.get_date_from_iso_str(
                event["historic_state"][0]["date"]
            )
            await events_mail.send_mail_event_report(
                loaders=loaders,
                group_name=group_name,
                event_id=event["event_id"],
                event_type=event_type,
                description=description,
                report_date=report_date,
            )
    else:
        LOGGER.info("- event report NOT sent")
        return


async def main() -> None:
    await send_event_report()
