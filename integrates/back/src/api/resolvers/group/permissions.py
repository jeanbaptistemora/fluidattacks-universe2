from .schema import (
    GROUP,
)
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
from sessions import (
    domain as sessions_domain,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_group_permissions(
    loaders: Dataloaders, email: str, group_name: str
) -> set[str]:
    if not group_name:
        raise InvalidParameter()

    return await authz.get_group_level_actions(loaders, email, group_name)


@GROUP.field("permissions")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
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
