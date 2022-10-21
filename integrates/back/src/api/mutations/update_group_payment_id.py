# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    PaymentMethod,
)
from custom_exceptions import (
    InvalidPaymentBusinessName,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    turn_args_into_kwargs,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@turn_args_into_kwargs
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    payment_id: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    group: Group = await loaders.group.load(group_name)
    org: Organization = await loaders.organization.load(group.organization_id)
    payment_methods = await billing_domain.customer_payment_methods(org=org)
    payment_method: PaymentMethod = list(
        filter(
            lambda method: method.id == payment_id,
            payment_methods,
        )
    )[0]
    if (
        payment_method.business_name.lower()
        != str(group.business_name).lower()
    ):
        raise InvalidPaymentBusinessName()
    managed: GroupManaged = (
        GroupManaged("UNDER_REVIEW")
        if payment_method.last_four_digits == ""
        else GroupManaged("NOT_MANAGED")
    )

    await groups_domain.update_group_payment_id(
        group=group,
        comments=comments,
        group_name=group_name,
        managed=managed,
        payment_id=payment_id,
        email=user_email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Updated managed in group {group_name} successfully",
    )

    return SimplePayload(success=True)
