from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidParameter,
    PermissionDenied,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from db_model.groups.enums import (
    GroupLanguage,
)
from db_model.groups.types import (
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
    description: str,
    group_name: str,
    language: str,
    **parameters: str,
) -> SimplePayloadType:
    group_name = group_name.lower()
    try:
        business_id = parameters.get("business_id", None)
        business_name = parameters.get("business_name", None)
        description = description.strip()
        if not description:
            raise InvalidParameter()
        if business_id is not None:
            validations_utils.validate_field_length(business_id, 60)
        if business_name is not None:
            validations_utils.validate_field_length(business_name, 60)
        validations_utils.validate_field_length(description, 200)
        validations_utils.validate_group_language(language)
        await groups_domain.update_metadata_typed(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(
                business_id=business_id,
                business_name=business_name,
                description=description,
                language=GroupLanguage[language.upper()],
            ),
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted to update group "
            f"{group_name}",
        )
        raise

    return SimplePayloadType(success=True)
