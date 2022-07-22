from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)


@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Stakeholder, ...]:
    loaders: Dataloaders = info.context.loaders
    # The store is needed to resolve stakeholder's role
    request_store = token_utils.get_request_store(info.context)
    request_store["entity"] = "ORGANIZATION"
    request_store["organization_id"] = parent.id

    return await orgs_domain.get_stakeholders(loaders, parent.id)
