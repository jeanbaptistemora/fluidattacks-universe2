from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupMetadataToUpdate,
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
    validations as validations_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayloadType:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    group: Group = await loaders.group.load(group_name)
    try:
        disambiguation = validations_utils.validate_markdown(
            kwargs.get("disambiguation", "")
        )
        await groups_domain.update_metadata(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(
                disambiguation=disambiguation,
            ),
            organization_id=group.organization_id,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted to update group "
            f"{group_name}",
        )
        raise

    return SimplePayloadType(success=True)
