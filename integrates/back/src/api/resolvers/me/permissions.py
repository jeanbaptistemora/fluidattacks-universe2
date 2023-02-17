from .schema import (
    ME,
)
import authz
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from typing import (
    Any,
)

# Constants
LOGGER = logging.getLogger(__name__)


@ME.field("permissions")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: str
) -> set[str]:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    permissions: set[str] = await authz.get_user_level_actions(
        loaders, user_email
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_user_permissions",
            extra=dict(extra=locals()),
        )

    return permissions
