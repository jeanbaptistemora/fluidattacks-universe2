from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.events.types import (
    Event,
)
from events import (
    domain as events_domain,
)
import logging
from mailer import (
    events as events_mail,
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def days_to_date(date: datetime) -> int:
    days = (datetime_utils.get_utc_now() - date).days

    return days


async def send_event_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = [
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        ]

    unsolved_events = [
        event
        for group in groups_names
        for event in await events_domain.get_unsolved_events(loaders, group)
    ]

    events_filtered: list[Event] = [
        event
        for event in unsolved_events
        if days_to_date(event.state.modified_date) in [7, 30]
    ]

    if events_filtered:
        for event in events_filtered:
            await events_mail.send_mail_event_report(
                loaders=loaders,
                group_name=event.group_name,
                event_id=event.id,
                event_type=event.type,
                description=event.description,
                root_id=event.root_id,
                reminder_notification=True,
                report_date=event.event_date.date(),
            )
    else:
        LOGGER.info("- event report NOT sent")


async def main() -> None:
    await send_event_report()
