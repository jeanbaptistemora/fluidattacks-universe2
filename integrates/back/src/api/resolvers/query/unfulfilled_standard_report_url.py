# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    RequiredNewPhoneNumber,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from reports import (
    domain as reports_domain,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from typing import (
    Any,
    Optional,
)
from verify import (
    operations as verify_operations,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    verification_code: str,
    **_kwargs: Any,
) -> str:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    stakeholder_email: str = user_info["user_email"]
    stakeholder: Stakeholder = await loaders.stakeholder.load(
        stakeholder_email
    )
    user_phone: Optional[StakeholderPhone] = stakeholder.phone
    if not user_phone:
        raise RequiredNewPhoneNumber()

    await verify_operations.check_verification(
        phone_number=get_international_format_phone_number(user_phone),
        code=verification_code,
    )
    return await reports_domain.get_signed_unfulfilled_standard_report_url(
        loaders=loaders,
        group_name=group_name,
        stakeholder_email=stakeholder_email,
    )
