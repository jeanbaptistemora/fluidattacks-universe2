from batch.dal import (
    delete_action,
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    Root,
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


async def remove_group_resources(*, item: BatchProcessing) -> None:
    group_name = item.entity
    email = item.subject
    message = f"Removing resources requested by {email} for group {group_name}"
    LOGGER.info(
        ":".join([item.subject, message]), extra={"extra": {"action": item}}
    )

    loaders: Dataloaders = get_new_context()
    # Get root info
    group_roots: tuple[Root, ...] = await loaders.group_roots.load(group_name)

    success: bool = True
    await groups_domain.remove_resources(
        loaders=loaders,
        group_name=group_name,
        email=email,
    )
    # Delete roots and related cloned repos
    if group_roots:
        root_removal = await put_action(
            action=Action.REMOVE_ROOTS,
            entity=group_name,
            subject=email,
            additional_info=",".join(
                [root.state.nickname for root in group_roots]
            ),
            queue=IntegratesBatchQueue.SMALL,
            product_name=Product.INTEGRATES,
        )
        success = root_removal.success
    message = f"Removal result: {success}"
    LOGGER.info(
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
