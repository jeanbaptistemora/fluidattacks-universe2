from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def remove_group_resources(*, item: BatchProcessing) -> None:
    group_name = item.entity
    user_email = item.subject
    message = (
        f"Removing resources requested by {user_email} for group {group_name}"
    )
    LOGGER_CONSOLE.info(
        ":".join([item.subject, message]), extra={"extra": {"action": item}}
    )

    loaders: Dataloaders = get_new_context()
    success = await groups_domain.remove_resources(
        loaders=loaders,
        group_name=group_name,
    )
    message = f"Removal result: {success}"
    LOGGER_CONSOLE.info(
        ":".join([item.subject, message]),
        extra={"extra": {"action": item, "success": success}},
    )

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
