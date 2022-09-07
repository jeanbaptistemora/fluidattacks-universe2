# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    DocumentNotFound,
    RequiredNewPhoneNumber,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
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
    logs as logs_utils,
)
from newutils.token import (
    get_jwt_content,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from typing import (
    Optional,
)
from verify.operations import (
    check_verification,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    verification_code: Optional[str],
    **_kwargs: None,
) -> str:
    logs_utils.cloudwatch_log(
        info.context,
        "Security: Attempted to get vulnerabilities for organization"
        f": {parent.id} at {datetime_utils.get_now()}",
    )
    if parent.vulnerabilities_url is None:
        raise DocumentNotFound()

    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    user_phone: Optional[StakeholderPhone] = stakeholder.phone
    if not user_phone:
        raise RequiredNewPhoneNumber()

    await check_verification(
        phone_number=get_international_format_phone_number(user_phone),
        code=verification_code or "",
    )

    logs_utils.cloudwatch_log(
        info.context,
        "Security: Get vulnerabilities for organization"
        f": {parent.id} at {datetime_utils.get_now()}",
    )
    return parent.vulnerabilities_url
