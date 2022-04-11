import authz
from custom_exceptions import (
    InvalidParameter,
)
from custom_types import (
    Organization,
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
    cast,
    Dict,
    Set,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_org_permissions(
    user_email: str, identifier: str, with_cache: bool
) -> Set[str]:
    # Exception: WF(Cannot assign to accepted value)
    actions: Set[str] = set()  # NOSONAR
    if identifier:
        actions = await authz.get_organization_level_actions(
            user_email, identifier, with_cache
        )
    else:
        raise InvalidParameter()
    return actions


async def resolve(
    parent: Organization, info: GraphQLResolveInfo, **kwargs: Dict
) -> Set[str]:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    org_id: str = parent["id"]
    identifier: str = cast(str, kwargs.get("identifier", org_id))

    permissions: Set[str] = await _get_org_permissions(
        user_email, identifier, with_cache=True
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_org_permissions with cache",
            extra=dict(extra=locals()),
        )
        await authz.revoke_cached_subject_policies(user_email)
        permissions = await _get_org_permissions(
            user_email, identifier, with_cache=False
        )
        if not permissions:
            LOGGER.error(
                "Empty permissions on _get_org_permissions without cache",
                extra=dict(extra=locals()),
            )
    return permissions
