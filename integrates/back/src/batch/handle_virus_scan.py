from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
import logging
import logging.config
from newutils import (
    resources as resources_utils,
    virus_scan,
)
from resources import (
    domain as resources_domain,
)
from settings import (
    LOGGING,
    NOEXTRA,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def handle_virus_scan(*, item: BatchProcessing) -> None:
    file_name = item.entity
    group_name = item.additional_info
    user_email = item.subject
    message = (
        f"Processing virus scan on file {file_name} requested by "
        f"{user_email} for group {group_name}"
    )
    LOGGER.info(":".join([item.subject, message]), **NOEXTRA)

    resource_file = await resources_utils.get_file(
        item.entity, item.additional_info
    )

    with open(resource_file, "r") as file:
        scanned_file_result = virus_scan.scan_file(
            file, user_email, group_name
        )

    if scanned_file_result:
        await resources_domain.update_group_files(
            file_name,
            group_name,
        )
    else:
        await resources_utils.remove_file(file_name)

    await delete_action(
        action_name=item.action_name,
        additional_info=group_name,
        entity=file_name,
        subject=user_email,
        time=item.time,
    )
