from .schema import (
    QUERY,
)
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
    InvalidDate,
    InvalidReportFilter,
    ReportAlreadyRequested,
    RequestedReportError,
    RequiredNewPhoneNumber,
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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.utils import (
    get_inverted_treatment_converted,
)
from decimal import (
    Decimal,
)
from decorators import (
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from newutils.datetime import (
    get_now,
)
from newutils.findings import (
    is_valid_finding_title,
)
from newutils.validations import (
    validate_field_length_deco,
    validate_fields_deco,
)
from newutils.vulnerabilities import (
    get_inverted_state_converted,
)
from organizations.domain import (
    validate_max_acceptance_severity,
    validate_min_acceptance_severity,
)
import pytz
from sessions import (
    domain as sessions_domain,
)
from settings import (
    TIME_ZONE,
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

MIN_VALUE = int(0)
MAX_VALUE = int(10000)


class EncodeDecimal(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return str(o)

        return json.JSONEncoder.default(self, o)


def _filter_unique_report(
    *,
    old_additional_info: str,
    new_type: str,
    new_treatments: set[VulnerabilityTreatmentStatus],
    new_states: set[VulnerabilityStateStatus],
    new_verifications: set[VulnerabilityVerificationStatus],
    new_closing_date: datetime | None,
    new_finding_title: str,
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
            and (new_closing_date.isoformat() if new_closing_date else None)
            == additional_info.get("closing_date", None)
            and new_finding_title == additional_info.get("finding_title", "")
        )

    return new_type == additional_info.get("report_type")


@validate_fields_deco(["location"])
@validate_field_length_deco("location", limit=100, is_greater_than_limit=False)
@enforce_group_level_auth_async
# noqa pylint: disable=too-many-locals
async def _get_url_group_report(
    *,
    info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    group_name: str,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
    verifications: set[VulnerabilityVerificationStatus],
    closing_date: datetime | None,
    finding_title: str,
    age: int | None,
    min_severity: Decimal | None,
    max_severity: Decimal | None,
    last_report: int | None,
    min_release_date: datetime | None,
    max_release_date: datetime | None,
    location: str,
    verification_code: str,
) -> bool:
    existing_actions: tuple[
        BatchProcessing, ...
    ] = await batch_dal.get_actions_by_name("report", group_name)

    if list(
        filter(
            lambda x: x.subject.lower() == user_email.lower()
            and _filter_unique_report(
                old_additional_info=x.additional_info,
                new_type=report_type,
                new_treatments=treatments,
                new_states=states,
                new_verifications=verifications,
                new_closing_date=closing_date,
                new_finding_title=finding_title,
            ),
            existing_actions,
        )
    ):
        raise ReportAlreadyRequested()
    loaders: Dataloaders = info.context.loaders
    stakeholder = await loaders.stakeholder.load(user_email)
    user_phone = stakeholder.phone if stakeholder else None
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
            "closing_date": closing_date.isoformat() if closing_date else None,
            "finding_title": finding_title,
            "age": age,
            "min_severity": min_severity,
            "max_severity": max_severity,
            "last_report": last_report,
            "min_release_date": min_release_date.isoformat()
            if min_release_date
            else None,
            "max_release_date": max_release_date.isoformat()
            if max_release_date
            else None,
            "location": location,
        },
        cls=EncodeDecimal,
    )

    success: bool = (
        await batch_dal.put_action(
            action=Action.REPORT,
            entity=group_name,
            subject=user_email,
            additional_info=additional_info,
            vcpus=4,
            attempt_duration_seconds=7200,
            queue=batch_dal.IntegratesBatchQueue.MEDIUM,
            product_name=Product.INTEGRATES,
            memory=7600,
        )
    ).success
    if not success:
        raise RequestedReportError()
    return success


def _validate_closing_date(*, closing_date: datetime | None) -> None:
    if closing_date is None:
        return
    tzn = pytz.timezone(TIME_ZONE)
    today = get_now()
    if closing_date.astimezone(tzn) > today:
        raise InvalidDate()


def _validate_days(field: int | None) -> None:
    if field and (MIN_VALUE > field or field > MAX_VALUE):
        raise InvalidReportFilter(
            f"Age value must be between {MIN_VALUE} and {MAX_VALUE}"
        )


def _validate_min_severity(**kwargs: Any) -> None:
    min_severity: Decimal | None = kwargs.get("min_severity", None)
    if min_severity is not None:
        validate_min_acceptance_severity(Decimal(min_severity))


def _validate_max_severity(**kwargs: Any) -> None:
    max_severity: Decimal | None = kwargs.get("max_severity", None)
    if max_severity is not None:
        validate_max_acceptance_severity(Decimal(max_severity))


def _get_severity_value(field: float | None) -> Decimal | None:
    if field is not None:
        return Decimal(field).quantize(Decimal("0.1"))
    return None


async def _get_finding_title(
    loaders: Dataloaders, finding_title: str | None
) -> str:
    if finding_title:
        await is_valid_finding_title(loaders, finding_title)
        return finding_title[:3]
    return ""


@QUERY.field("report")
@convert_kwargs_to_snake_case
@require_login
async def resolve(  # pylint: disable=too-many-locals
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    verification_code: str,
    **kwargs: Any,
) -> dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    report_type: str = kwargs["report_type"]
    if report_type == "CERT":
        group: Group = await loaders.group.load(group_name)
        if not group.state.has_machine:
            raise RequestedReportError(
                expr="Group must have Machine enabled to generate Certificates"
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
        user_role = await authz.get_group_level_role(
            loaders, user_email, group_name
        )
        if user_role != "user_manager":
            raise RequestedReportError(
                expr="Only user managers can request certificates"
            )
    states: set[VulnerabilityStateStatus] = (
        {
            VulnerabilityStateStatus[get_inverted_state_converted(state)]
            for state in kwargs["states"]
        }
        if kwargs.get("states")
        else set(
            [
                VulnerabilityStateStatus["SAFE"],
                VulnerabilityStateStatus["VULNERABLE"],
            ]
        )
    )
    treatments: set[VulnerabilityTreatmentStatus] = (
        {
            VulnerabilityTreatmentStatus[
                get_inverted_treatment_converted(treatment)
            ]
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
    closing_date: datetime | None = kwargs.get("closing_date", None)
    finding_title: str = await _get_finding_title(
        loaders, kwargs.get("finding_title")
    )
    if closing_date is not None:
        _validate_closing_date(closing_date=closing_date)
        states = set(
            [
                VulnerabilityStateStatus["SAFE"],
            ]
        )
        treatments = set(VulnerabilityTreatmentStatus)
        if verifications != set(
            [
                VulnerabilityVerificationStatus["VERIFIED"],
            ]
        ):
            verifications = set()
    min_severity: Decimal | None = _get_severity_value(
        kwargs.get("min_severity")
    )
    max_severity: Decimal | None = _get_severity_value(
        kwargs.get("max_severity")
    )
    _validate_closing_date(closing_date=kwargs.get("min_release_date", None))
    _validate_days(kwargs.get("age", None))
    _validate_min_severity(**kwargs)
    _validate_max_severity(**kwargs)
    _validate_days(kwargs.get("last_report", None))
    _validate_closing_date(closing_date=kwargs.get("max_release_date", None))

    return {
        "success": await _get_url_group_report(
            info=info,
            report_type=report_type,
            user_email=user_email,
            group_name=group_name,
            treatments=treatments,
            states=states,
            verifications=verifications,
            closing_date=closing_date,
            finding_title=finding_title,
            age=kwargs.get("age", None),
            min_severity=min_severity,
            max_severity=max_severity,
            last_report=kwargs.get("last_report", None),
            min_release_date=kwargs.get("min_release_date", None),
            max_release_date=kwargs.get("max_release_date", None),
            location=kwargs.get("location", ""),
            verification_code=verification_code,
        )
    }
