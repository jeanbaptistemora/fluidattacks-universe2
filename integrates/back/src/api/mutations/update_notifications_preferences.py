from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidCvssField,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.stakeholders.utils import (
    format_notifications_preferences,
)
from decimal import (
    Decimal,
    InvalidOperation,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders.domain import (
    update_notification_preferences,
)
from typing import (
    Any,
)


@MUTATION.field("updateNotificationsPreferences")
@convert_kwargs_to_snake_case
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    notifications_preferences: dict[str, Any],
) -> SimplePayload:
    loaders = info.context.loaders
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    if notifications_preferences.get("parameters", False):
        try:
            min_severity = Decimal(
                str(notifications_preferences["parameters"]["min_severity"])
            )
            notifications_preferences.update(
                {"parameters": {"min_severity": min_severity}}
            )
        except InvalidOperation as ex:
            raise InvalidCvssField() from ex
    else:
        stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
        cvss = (
            stakeholder.state.notifications_preferences.parameters.min_severity
        )
        notifications_preferences.update(
            {"parameters": {"min_severity": Decimal(cvss)}}
        )

    await update_notification_preferences(
        email=user_email,
        preferences=format_notifications_preferences(
            notifications_preferences
        ),
    )

    return SimplePayload(success=True)
