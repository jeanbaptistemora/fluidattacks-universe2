from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from urllib.parse import (
    unquote_plus,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("url")
def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str:

    return unquote_plus(parent.url)
