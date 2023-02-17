from .schema import (
    ORGANIZATION,
)
import authz
from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.types import (
    Organization,
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


async def _get_org_permissions(
    loaders: Dataloaders, user_email: str, organization_id: str
) -> set[str]:
    if not organization_id:
        raise InvalidParameter()

    return await authz.get_organization_level_actions(
        loaders, user_email, organization_id
    )


@ORGANIZATION.field("permissions")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    loaders: Dataloaders = get_new_context()
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    permissions: set[str] = await _get_org_permissions(
        loaders, user_email, parent.id
    )
    if not permissions:
        LOGGER.error(
            "Empty permissions on _get_org_permissions",
            extra=dict(extra=locals()),
        )
    return permissions
