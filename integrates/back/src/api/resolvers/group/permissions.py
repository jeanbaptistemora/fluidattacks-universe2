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
from typing import (
    Any,
    Dict,
    Set,
    Union,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_group_permissions(
    user_email: str, group_name: str, with_cache: bool
) -> Set[str]:
    if not group_name:
        raise InvalidParameter()
    actions: Set[str] = await authz.get_group_level_actions(
        user_email, group_name, with_cache
    )
    return actions


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Set[str]:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
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
