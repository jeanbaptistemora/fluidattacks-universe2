import authz
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from typing import (
    Any,
    Dict,
    Set,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_user_permissions(user_email: str, with_cache: bool) -> Set[str]:
    actions: Set[str] = await authz.get_user_level_actions(
        user_email, with_cache
    )
    return actions


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: str
) -> Set[str]:
    user_email = str(parent["user_email"])

    permissions: Set[str] = await _get_user_permissions(
        user_email, with_cache=True
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_user_permissions with cache",
            extra=dict(extra=locals()),
        )
        await authz.revoke_cached_subject_policies(user_email)
        permissions = await _get_user_permissions(user_email, with_cache=False)
        if not permissions:
            LOGGER.error(
                "Empty permissions on _get_user_permissions without cache",
                extra=dict(extra=locals()),
            )
    return permissions
