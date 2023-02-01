from api.mutations import (
    SimpleGroupPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    tags: list[str],
) -> SimpleGroupPayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]

    if not await groups_domain.is_valid(loaders, group_name):
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to add tags without the allowed validations",
        )
        raise ErrorUpdatingGroup.new()

    if not await groups_domain.validate_group_tags(loaders, group_name, tags):
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to add tags without allowed structure",
        )
        raise ErrorUpdatingGroup.new()

    await groups_domain.add_tags(
        loaders=loaders,
        email=email,
        group=await loaders.group.load(group_name),
        tags_to_add=set(tags),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Tags added to {group_name} group successfully",
    )

    loaders.group.clear(group_name)
    group = await loaders.group.load(group_name)

    return SimpleGroupPayload(success=True, group=group)
