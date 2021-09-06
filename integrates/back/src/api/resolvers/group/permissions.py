import authz
from custom_exceptions import (
    InvalidParameter,
)
from custom_types import (
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
from settings import (
    LOGGING,
)
from typing import (
    Dict,
    Set,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_group_permissions(
    user_email: str, group_name: str, with_cache: bool
) -> Set[str]:
    # Exception: WF(Cannot assign to accepted value)
    actions: Set[str] = set()  # NOSONAR
    if group_name:
        actions = await authz.get_group_level_actions(
            user_email, group_name, with_cache
        )
    else:
        raise InvalidParameter()
    return actions


async def resolve(parent: Group, info: GraphQLResolveInfo) -> Set[str]:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = parent["name"]

    permissions: Set[str] = await _get_group_permissions(
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
