from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
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
)
from custom_types import (
    Report,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from decorators import (
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from newutils import (
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Dict,
    Set,
    Tuple,
)


def _filter_unique_report(
    old_additional_info: str,
    new_type: str,
    new_treatments: Set[VulnerabilityTreatmentStatus],
) -> bool:
    additional_info: Dict[str, Any] = json.loads(old_additional_info)
    if new_type == "XLS":
        return new_type == additional_info.get("report_type") and list(
            sorted(new_treatments)
        ) == list(sorted(additional_info.get("treatments", [])))

    return new_type == additional_info.get("report_type")


@enforce_group_level_auth_async
async def _get_url_group_report(
    _info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    group_name: str,
    treatments: Set[VulnerabilityTreatmentStatus],
) -> bool:
    additional_info: str = json.dumps(
        {
            "report_type": report_type,
            "treatments": list(sorted(treatments)),
        }
    )
    existing_actions: Tuple[
        BatchProcessing, ...
    ] = await batch_dal.get_actions_by_name("report", group_name)

    if list(
        filter(
            lambda x: x.subject.lower() == user_email.lower()
            and _filter_unique_report(
                x.additional_info, report_type, treatments
            ),
            existing_actions,
        )
    ):
        raise ReportAlreadyRequested()

    success: bool = (
        await batch_dal.put_action(
            action=Action.REPORT,
            entity=group_name,
            subject=user_email,
            additional_info=additional_info,
            vcpus=4,
            attempt_duration_seconds=7200,
            queue="reports_soon",
            product_name=Product.INTEGRATES,
            memory=7200,
        )
    ).success
    if not success:
        raise RequestedReportError()
    return success


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> Report:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = get_key_or_fallback(kwargs)
    report_type: str = kwargs["report_type"]
    treatments = (
        {
            VulnerabilityTreatmentStatus[treatment]
            for treatment in kwargs["treatments"]
        }
        if kwargs.get("treatments")
        else set(VulnerabilityTreatmentStatus)
    )

    return {
        "success": await _get_url_group_report(
            info,
            report_type,
            user_email,
            group_name=group_name,
            treatments=treatments,
        )
    }
