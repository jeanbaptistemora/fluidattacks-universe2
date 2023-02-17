from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidParameter,
    RequiredNewPhoneNumber,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from reports import (
    domain as reports_domain,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from typing import (
    Any,
)
from verify import (
    operations as verify_operations,
)


@QUERY.field("unfulfilledStandardReportUrl")
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
    **kwargs: Any,
) -> str:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    stakeholder_email: str = user_info["user_email"]
    stakeholder = await loaders.stakeholder.load(stakeholder_email)
    user_phone = stakeholder.phone if stakeholder else None
    if not user_phone:
        raise RequiredNewPhoneNumber()

    await verify_operations.check_verification(
        phone_number=get_international_format_phone_number(user_phone),
        code=verification_code,
    )
    unfulfilled_standards = (
        set(kwargs["unfulfilled_standards"])
        if "unfulfilled_standards" in kwargs
        else None
    )
    if not unfulfilled_standards and unfulfilled_standards is not None:
        raise InvalidParameter("unfulfilledStandards")
    return await reports_domain.get_signed_unfulfilled_standard_report_url(
        loaders=loaders,
        group_name=group_name,
        stakeholder_email=stakeholder_email,
        unfulfilled_standards=unfulfilled_standards,
    )
