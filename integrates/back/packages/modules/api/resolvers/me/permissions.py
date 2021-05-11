
import logging
import logging.config
from typing import (
    Set,
    cast,
)

from graphql.type.definition import GraphQLResolveInfo

import authz
from back.settings import LOGGING
from custom_exceptions import InvalidParameter
from custom_types import Me


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_permissions(
    user_email: str,
    entity: str,
    identifier: str,
    with_cache: bool
) -> Set[str]:
    actions: Set[str] = set()
    if entity == 'USER':
        actions = await authz.get_user_level_actions(user_email, with_cache)
    elif entity == 'PROJECT' and identifier:
        actions = await authz.get_group_level_actions(
            user_email,
            identifier,
            with_cache
        )
    elif entity == 'ORGANIZATION' and identifier:
        actions = await authz.get_organization_level_actions(
            user_email,
            identifier,
            with_cache
        )
    else:
        raise InvalidParameter()
    return actions


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> Set[str]:
    user_email: str = cast(str, parent['user_email'])
    entity: str = kwargs['entity']
    identifier: str = kwargs.get('identifier', '')

    permissions: Set[str] = await _get_permissions(
        user_email,
        entity,
        identifier,
        with_cache=True
    )
    if not permissions:
        LOGGER.error(
            'Empty permissions on _get_permissions with cache',
            extra=dict(extra=locals())
        )
        await authz.revoke_cached_subject_policies(user_email)
        permissions = await _get_permissions(
            user_email,
            entity,
            identifier,
            with_cache=False
        )
        if not permissions:
            LOGGER.error(
                'Empty permissions on _get_permissions without cache',
                extra=dict(extra=locals())
            )
    return permissions
