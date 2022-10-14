# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidCvssField,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
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
    loaders = info.context.loaders
    user_info = await token_utils.get_jwt_content(info.context)
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
        cvss = stakeholder.notifications_preferences.parameters.min_severity
        notifications_preferences.update(
            {"parameters": {"min_severity": Decimal(cvss)}}
        )

    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            notifications_preferences=format_notifications_preferences(
                notifications_preferences
            )
        ),
    )
    return SimplePayload(success=True)
