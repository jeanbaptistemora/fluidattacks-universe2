from .payloads.types import (
    SimpleGroupPayload,
)
from .schema import (
    MUTATION,
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


@MUTATION.field("removeGroupTag")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    tag: str,
) -> SimpleGroupPayload:
    group_name = group_name.lower()
    loaders: Dataloaders = info.context.loaders
    group = await groups_domain.get_group(loaders, group_name)
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]

    if await groups_domain.is_valid(loaders, group_name) and group.state.tags:
        await groups_domain.remove_tag(
            loaders=loaders,
            email=email,
            group=group,
            tag_to_remove=tag,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed tag from {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove tag in {group_name} group",
        )
        raise ErrorUpdatingGroup.new()

    loaders.group.clear(group_name)
    group = await groups_domain.get_group(loaders, group_name)

    return SimpleGroupPayload(success=True, group=group)
