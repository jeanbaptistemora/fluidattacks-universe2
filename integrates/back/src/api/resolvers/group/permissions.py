import authz
from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    token as token_utils,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_group_permissions(
    loaders: Dataloaders, email: str, group_name: str
) -> set[str]:
    if not group_name:
        raise InvalidParameter()
    actions: set[str] = await authz.get_group_level_actions(
        loaders, email, group_name
    )
    return actions


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = parent.name
    permissions: set[str] = await _get_group_permissions(
        loaders, user_email, group_name
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_group_permissions",
            extra=dict(extra=locals()),
        )

    return permissions
