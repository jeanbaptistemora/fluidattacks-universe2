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
    Group as BillingGroup,
    GroupAuthors,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_service_white,
    require_login,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> BillingGroup:
    group_name: str = str(kwargs["group_name"]).lower()
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(group_name.lower())

    group_authors: GroupAuthors = await billing_domain.get_group_authors(
        date=kwargs.get("date", datetime_utils.get_now()),
        group=group,
    )

    return BillingGroup(
        current_spend=group_authors.current_spend,
        total=group_authors.total,
        authors=group_authors.data,
    )
