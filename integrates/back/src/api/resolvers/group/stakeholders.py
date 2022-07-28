from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    get_group_stakeholders_emails,
)
from newutils import (
    token as token_utils,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Stakeholder, ...]:
    loaders: Dataloaders = info.context.loaders
    # The store is needed to resolve stakeholder's role
    request_store = token_utils.get_request_store(info.context)
    request_store["entity"] = "GROUP"
    request_store["group_name"] = parent.name
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    stakeholderes_emails: list[str] = await get_group_stakeholders_emails(
        loaders, parent.name
    )
    stakeholders: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(stakeholderes_emails)

    exclude_fluid_staff = not stakeholders_domain.is_fluid_staff(user_email)
    if exclude_fluid_staff:
        stakeholders = tuple(
            stakeholder
            for stakeholder in stakeholders
            if not stakeholders_domain.is_fluid_staff(stakeholder.email)
        )

    return stakeholders
