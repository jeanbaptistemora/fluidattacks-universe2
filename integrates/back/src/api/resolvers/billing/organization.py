# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    Organization,
    OrganizationAuthors,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_organization_level_auth_async,
    require_login,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> Organization:
    organization_authors: OrganizationAuthors = (
        await billing_domain.get_organization_authors(
            date=kwargs.get("date", datetime_utils.get_now()),
            org_id=kwargs["organization_id"],
            loaders=info.context.loaders,
        )
    )

    return Organization(
        authors=organization_authors.data,
        current_spend=organization_authors.current_spend,
        total=organization_authors.total,
        portal="",
    )
