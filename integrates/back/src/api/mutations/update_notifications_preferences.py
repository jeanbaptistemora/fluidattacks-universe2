from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Me,
    SimplePayload,
)
from db_model import (
    users as user_model,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    parent: Me,
    notifications_preferences: Dict[str, Any],
    **_kwargs: None,
) -> SimplePayload:
    user_email: str = parent["user_email"]

    await user_model.update_user(
        user_email=user_email,
        notifications_preferences=notifications_preferences,
    )
    return SimplePayload(success=True)
