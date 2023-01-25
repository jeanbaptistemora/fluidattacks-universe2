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
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)


@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Stakeholder]:
    loaders: Dataloaders = info.context.loaders
    # The store is needed to resolve stakeholder's role
    request_store = sessions_domain.get_request_store(info.context)
    request_store["entity"] = "ORGANIZATION"
    request_store["organization_id"] = parent.id

    return await orgs_domain.get_stakeholders(loaders, parent.id)
