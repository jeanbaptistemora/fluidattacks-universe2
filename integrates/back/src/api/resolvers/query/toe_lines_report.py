from .schema import (
    QUERY,
)
from api.resolvers.query.report import (
    filter_unique_report,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    get_actions_by_name,
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    ReportAlreadyRequested,
    RequestedReportError,
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
import json
from sessions.domain import (
    get_jwt_content,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from typing import (
    Any,
)
from verify.operations import (
    check_verification,
)


@QUERY.field("toeLinesReport")
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
) -> dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await get_jwt_content(info.context)
    stakeholder_email: str = user_info["user_email"]
    stakeholder = await loaders.stakeholder.load(stakeholder_email)
    user_phone = stakeholder.phone if stakeholder else None
    if not user_phone:
        raise RequiredNewPhoneNumber()

    existing_actions: tuple[BatchProcessing, ...] = await get_actions_by_name(
        "report", group_name
    )
    if list(
        filter(
            lambda x: x.subject.lower() == stakeholder_email.lower()
            and filter_unique_report(
                old_additional_info=x.additional_info,
                new_type="TOE_LINES",
                new_treatments=set(),
                new_states=set(),
                new_verifications=set(),
                new_closing_date=None,
                new_finding_title="",
            ),
            existing_actions,
        )
    ):
        raise ReportAlreadyRequested()

    await check_verification(
        phone_number=get_international_format_phone_number(user_phone),
        code=verification_code,
    )

    additional_info: str = json.dumps(
        {
            "report_type": "TOE_LINES",
        },
    )

    success: bool = (
        await put_action(
            action=Action.REPORT,
            entity=group_name,
            subject=stakeholder_email,
            additional_info=additional_info,
            vcpus=4,
            attempt_duration_seconds=7200,
            queue=IntegratesBatchQueue.MEDIUM,
            product_name=Product.INTEGRATES,
            memory=7600,
        )
    ).success
    if not success:
        raise RequestedReportError()

    return {"success": success}
