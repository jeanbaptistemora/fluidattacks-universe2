# Standard
import logging
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.typing import (
    CreateOrganizationPayload,
    Organization,
)
from decorators import require_login
from organizations import domain as orgs_domain


# Constants
TRANSACTIONS_LOGGER: logging.Logger = logging.getLogger('transactional')


@require_login
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    name: str
) -> CreateOrganizationPayload:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    TRANSACTIONS_LOGGER.info(
        'User %s attempted to create organization with name %s',
        user_email,
        name
    )
    organization: Organization = await orgs_domain.create_organization(
        name,
        user_email
    )
    TRANSACTIONS_LOGGER.info(
        'Organization %s with ID %s was successfully created by %s',
        organization['name'],
        organization['id'],
        user_email
    )

    return CreateOrganizationPayload(success=True, organization=organization)
