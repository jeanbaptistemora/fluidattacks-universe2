from custom_types import (
    AddOrganizationPayload,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    Dict,
)

# Constants
TRANSACTIONS_LOGGER: logging.Logger = logging.getLogger("transactional")


@require_login
async def mutate(
    _parent: None, info: GraphQLResolveInfo, name: str
) -> AddOrganizationPayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    TRANSACTIONS_LOGGER.info(
        "User %s attempted to add a new organization with name %s",
        user_email,
        name,
    )
    organization: Dict[str, Any] = await orgs_domain.add_organization(
        name, user_email
    )
    TRANSACTIONS_LOGGER.info(
        "Organization %s with ID %s was successfully added by %s",
        organization["name"],
        organization["id"],
        user_email,
    )

    return AddOrganizationPayload(success=True, organization=organization)
