from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidDate,
    InvalidParameter,
    PermissionDenied,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
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
    datetime as datetime_utils,
    logs as logs_utils,
)
import pytz
from sessions import (
    domain as sessions_domain,
)
from settings import (
    TIME_ZONE,
)
from typing import (
    Any,
    Optional,
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
    **parameters: Any,
) -> SimplePayloadType:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    try:
        business_id = parameters.get("business_id")
        business_name = parameters.get("business_name")
        sprint_duration = parameters.get("sprint_duration")
        sprint_start_date: Optional[datetime] = parameters.get(
            "sprint_start_date"
        )
        description = description.strip()
        if not description:
            raise InvalidParameter()
        if sprint_start_date is not None:
            tzn = pytz.timezone(TIME_ZONE)
            today = datetime_utils.get_now()
            if sprint_start_date.astimezone(tzn) > today:
                raise InvalidDate()
        metadata = groups_domain.assign_metadata(
            business_id=business_id,
            business_name=business_name,
            description=description,
            language=language,
            sprint_start_date=sprint_start_date,
            sprint_duration=sprint_duration,
            tzn=tzn,
        )

        await groups_domain.update_group_info(
            loaders=loaders,
            group_name=group_name,
            metadata=metadata,
            email=user_email,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted to update group "
            f"{group_name}",
        )
        raise

    return SimplePayloadType(success=True)
