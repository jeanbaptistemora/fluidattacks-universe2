import authz
from custom_exceptions import (
    InvalidParameter,
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
    user_email: str, group_name: str, with_cache: bool
) -> set[str]:
    if not group_name:
        raise InvalidParameter()
    actions: set[str] = await authz.get_group_level_actions(
        user_email, group_name, with_cache
    )
    return actions


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = parent.name
    permissions: set[str] = await _get_group_permissions(
        user_email, group_name, with_cache=True
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_group_permissions with cache",
            extra=dict(extra=locals()),
        )
        await authz.revoke_cached_subject_policies(user_email)
        permissions = await _get_group_permissions(
            user_email, group_name, with_cache=False
        )
        if not permissions:
            LOGGER.error(
                "Empty permissions on _get_group_permissions without cache",
                extra=dict(extra=locals()),
            )
    return permissions
