# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.constants import (
    DEFAULT_MIN_SEVERITY,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if parent.policies:
        return parent.policies.min_breaking_severity or DEFAULT_MIN_SEVERITY

    organization: Organization = await info.context.loaders.organization.load(
        parent.organization_id
    )
    return organization.policies.min_breaking_severity or DEFAULT_MIN_SEVERITY
