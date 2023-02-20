from .schema import (
    ORGANIZATION,
)
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
    validations,
)
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)


@ORGANIZATION.field("stakeholders")
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

    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    stakeholders = await orgs_domain.get_stakeholders(loaders, parent.id)

    exclude_fluid_staff = not validations.is_fluid_staff(user_email)
    if exclude_fluid_staff:
        return [
            stakeholder
            for stakeholder in stakeholders
            if not validations.is_fluid_staff(stakeholder.email)
        ]

    return stakeholders
