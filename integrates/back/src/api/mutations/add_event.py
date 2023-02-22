from .payloads.types import (
    AddEventPayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    validations,
)
from sessions import (
    domain as sessions_domain,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)


@MUTATION.field("addEvent")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    image: UploadFile | None = None,
    file: UploadFile | None = None,
    **kwargs: Any,
) -> AddEventPayload:
    """Resolve add_event mutation."""
    user_info = await sessions_domain.get_jwt_content(info.context)
    hacker_email = user_info["user_email"]

    if file is not None:
        validations.validate_sanitized_csv_input(
            file.filename, file.content_type
        )
    if image is not None:
        validations.validate_sanitized_csv_input(
            image.filename, image.content_type
        )
    event_id = await events_domain.add_event(
        info.context.loaders,
        hacker_email=hacker_email,
        group_name=group_name.lower(),
        file=file,
        image=image,
        **kwargs,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added a new event in {group_name} group successfully",
    )

    return AddEventPayload(event_id=event_id, success=True)
