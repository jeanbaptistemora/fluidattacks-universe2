from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
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
    RequiredNewPhoneNumber,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
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
from stakeholders import (
    domain as stakeholders_domain,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from typing import (
    Any,
    Dict,
    Optional,
)
from verify import (
    operations as verify_operations,
)


def _filter_unique_report(
    old_additional_info: str,
    new_type: str,
    new_treatments: set[VulnerabilityTreatmentStatus],
    new_states: set[VulnerabilityStateStatus],
    new_verifications: set[VulnerabilityVerificationStatus],
) -> bool:
    additional_info: dict[str, Any] = json.loads(old_additional_info)
    if new_type == "XLS":
        return (
            new_type == additional_info.get("report_type")
            and list(sorted(new_treatments))
            == list(sorted(additional_info.get("treatments", [])))
            and list(sorted(new_states))
            == list(sorted(additional_info.get("states", [])))
            and list(sorted(new_verifications))
            == list(sorted(additional_info.get("verifications", [])))
        )

    return new_type == additional_info.get("report_type")


@enforce_group_level_auth_async
async def _get_url_group_report(  # pylint: disable = too-many-arguments
    _info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    group_name: str,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
    verifications: set[VulnerabilityVerificationStatus],
    verification_code: str,
) -> bool:
    existing_actions: tuple[
        BatchProcessing, ...
    ] = await batch_dal.get_actions_by_name("report", group_name)

    if list(
        filter(
            lambda x: x.subject.lower() == user_email.lower()
            and _filter_unique_report(
                x.additional_info,
                report_type,
                treatments,
                states,
                verifications,
            ),
            existing_actions,
        )
    ):
        raise ReportAlreadyRequested()

    user = await stakeholders_domain.get_by_email(user_email)
    user_phone: Optional[StakeholderPhone] = user["phone"]
    if not user_phone:
        raise RequiredNewPhoneNumber()

    await verify_operations.check_verification(
        phone_number=get_international_format_phone_number(user_phone),
        code=verification_code,
    )

    additional_info: str = json.dumps(
        {
            "report_type": report_type,
            "treatments": list(sorted(treatments)),
            "states": list(sorted(states)),
            "verifications": list(sorted(verifications)),
        }
    )

    success: bool = (
        await batch_dal.put_action(
            action=Action.REPORT,
            entity=group_name,
            subject=user_email,
            additional_info=additional_info,
            vcpus=4,
            attempt_duration_seconds=7200,
            queue="medium",
            product_name=Product.INTEGRATES,
            memory=7600,
        )
    ).success
    if not success:
        raise RequestedReportError()
    return success


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    verification_code: str,
    **kwargs: Any,
) -> Dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = get_key_or_fallback(kwargs)
    report_type: str = kwargs["report_type"]
    if report_type == "CERT":
        group: Group = await loaders.group.load(group_name)
        if not group.state.has_machine:
            raise RequestedReportError(
                expr=(
                    "Group must have Machine enabled to generate Certificates"
                )
            )
        if not (
            group.business_id and group.business_name and group.description
        ):
            raise RequestedReportError(
                expr=(
                    "Lacking required group information to generate the"
                    " certificate. Make sure the businessId, businessName "
                    " and description fields of the Group are filled out"
                )
            )
        user_role = await authz.get_group_level_role(user_email, group_name)
        if user_role != "user_manager":
            raise RequestedReportError(
                expr="Only user managers can request certificates"
            )
    states: set[VulnerabilityStateStatus] = (
        {VulnerabilityStateStatus[state] for state in kwargs["states"]}
        if kwargs.get("states")
        else set(
            [
                VulnerabilityStateStatus["CLOSED"],
                VulnerabilityStateStatus["OPEN"],
            ]
        )
    )
    treatments: set[VulnerabilityTreatmentStatus] = (
        {
            VulnerabilityTreatmentStatus[treatment]
            for treatment in kwargs["treatments"]
        }
        if kwargs.get("treatments")
        else set(VulnerabilityTreatmentStatus)
    )
    verifications: set[VulnerabilityVerificationStatus] = (
        {
            VulnerabilityVerificationStatus[verification]
            for verification in kwargs["verifications"]
        }
        if kwargs.get("verifications")
        else set()
    )

    return {
        "success": await _get_url_group_report(
            info,
            report_type,
            user_email,
            group_name=group_name,
            treatments=treatments,
            states=states,
            verifications=verifications,
            verification_code=verification_code,
        )
    }
