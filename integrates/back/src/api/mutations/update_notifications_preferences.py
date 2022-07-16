from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
)
from db_model.stakeholders.utils import (
    format_notifications_preferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    notifications_preferences: Dict[str, Any],
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            notifications_preferences=format_notifications_preferences(
                notifications_preferences
            )
        ),
    )
    return SimplePayload(success=True)
