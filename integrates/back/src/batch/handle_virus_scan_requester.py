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
import logging
import logging.config
from mailer.resources import (
    send_mail_handled_file,
)
from newutils import (
    resources as resources_utils,
)
from settings import (
    LOGGING,
    NOEXTRA,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def handle_virus_scan_requester(*, item: BatchProcessing) -> None:
    loaders: Dataloaders = get_new_context()
    group_name = item.entity
    file_name = item.additional_info
    user_email = item.subject
    message = (
        f"Processing virus scan on file {file_name} requested by "
        f"{user_email}"
    )
    LOGGER_CONSOLE.info(":".join([item.subject, message]), **NOEXTRA)

    handled_file = await resources_utils.get_file(
        file_name, group_name, user_email
    )

    if handled_file:
        await send_mail_handled_file(
            loaders,
            user_email,
            group_name,
            file_name,
            uploaded=True,
        )
    else:
        await resources_utils.remove_file(file_name)
        await send_mail_handled_file(
            loaders,
            user_email,
            group_name,
            file_name,
            uploaded=False,
        )

    await delete_action(
        action_name=item.action_name,
        additional_info=group_name,
        entity=file_name,
        subject=user_email,
        time=item.time,
    )
