# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.enrollment.types import (
    Enrollment,
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
) -> Enrollment:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    enrollment: Enrollment = await loaders.enrollment.load(user_email)
    return enrollment
