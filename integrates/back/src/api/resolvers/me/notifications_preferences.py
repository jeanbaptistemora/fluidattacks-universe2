# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> NotificationsPreferences:
    email = str(parent["user_email"])
    stakeholder: Stakeholder = await info.context.loaders.stakeholder.load(
        email
    )

    return stakeholder.state.notifications_preferences
