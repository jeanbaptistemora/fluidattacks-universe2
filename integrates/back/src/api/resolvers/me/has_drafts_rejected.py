# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
    has_rejected_drafts,
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
async def resolve(parent: dict[str, Any], info: GraphQLResolveInfo) -> bool:
    email: str = str(parent["user_email"])
    drafts: tuple[Finding, ...] = await info.context.loaders.me_drafts.load(
        email
    )

    return has_rejected_drafts(drafts=drafts)
