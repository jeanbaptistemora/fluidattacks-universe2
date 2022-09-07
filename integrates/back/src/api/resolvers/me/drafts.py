# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@require_login
async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Finding, ...]:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    drafts: tuple[Finding, ...] = await loaders.me_drafts.load(user_email)
    return drafts
