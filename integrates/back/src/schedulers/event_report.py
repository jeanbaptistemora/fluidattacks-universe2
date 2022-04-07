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
LOGGER_CONSOLE = logging.getLogger("console")


async def send_event_report() -> None:
    groups_names = await groups_domain.get_active_groups()

    if FI_ENVIRONMENT == "production":
        groups_names = [
            group.name
            for group in groups_names
            if group.name not in FI_TEST_PROJECTS.split(",")
        ]

    unsolved_events: List[EventType] = [
        await events_domain.get_unsolved_events(group)
        for group in groups_names
    ]

    # pylint: disable=simplifiable-condition
    events_filtered: List[EventType] = [
        event
        for event in unsolved_events
        if event != []
        and (
            (
                datetime_utils.get_now()
                - datetime_utils.get_datetime_from_iso_str(
                    event[0]["historic_state"][-1]["date"]
                )
            ).days
            == 7
            or 30
        )
    ]

    user_loaders = get_new_context()
    if events_filtered:
        for event in events_filtered:
            group_name = str(get_key_or_fallback(event[0], fallback=""))
            event_type = event[0]["event_type"]
            description = event[0]["detail"]
            await events_mail.send_mail_event_report(
                loaders=user_loaders,
                group_name=group_name,
                event_id=event[0]["event_id"],
                event_type=event_type,
                description=description,
            )
    else:
        LOGGER_CONSOLE.info("- event report NOT sent")
        return


async def main() -> None:
    await send_event_report()
