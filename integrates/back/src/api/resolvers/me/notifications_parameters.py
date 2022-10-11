# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: NotificationsPreferences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> NotificationsParameters:
    return parent.parameters
