from .payloads.types import (
    SimplePayload,
)
from api.mutations.schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    MachineCanNotOperate,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding31Severity,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingAttributesToAdd,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.availability import (
    operation_can_be_executed,
)
from newutils import (
    logs as logs_utils,
    requests as requests_utils,
)
from newutils.validations import (
    check_and_set_min_time_to_remediate,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addFinding")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
)
async def mutate(  # pylint: disable=too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    description: str,
    recommendation: str,
    title: str,
    threat: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    try:
        if not operation_can_be_executed(info.context, title):
            raise MachineCanNotOperate()

        await findings_domain.add_finding(
            loaders=loaders,
            group_name=group_name,
            stakeholder_email=stakeholder_email,
            attributes=FindingAttributesToAdd(
                attack_vector_description=kwargs["attack_vector_description"],
                description=description,
                min_time_to_remediate=check_and_set_min_time_to_remediate(
                    kwargs.get("min_time_to_remediate", None)
                ),
                recommendation=recommendation,
                severity=Finding31Severity(
                    attack_complexity=Decimal(
                        str(kwargs["attack_complexity"])
                    ),
                    attack_vector=Decimal(str(kwargs["attack_vector"])),
                    availability_impact=Decimal(
                        str(kwargs["availability_impact"])
                    ),
                    availability_requirement=Decimal(
                        str(kwargs["availability_requirement"])
                    ),
                    confidentiality_impact=Decimal(
                        str(kwargs["confidentiality_impact"])
                    ),
                    confidentiality_requirement=Decimal(
                        str(kwargs["confidentiality_requirement"])
                    ),
                    exploitability=Decimal(str(kwargs["exploitability"])),
                    integrity_impact=Decimal(str(kwargs["integrity_impact"])),
                    integrity_requirement=Decimal(
                        str(kwargs["integrity_requirement"])
                    ),
                    modified_attack_complexity=Decimal(
                        str(kwargs["modified_attack_complexity"])
                    ),
                    modified_attack_vector=Decimal(
                        str(kwargs["modified_attack_vector"])
                    ),
                    modified_availability_impact=Decimal(
                        str(kwargs["modified_availability_impact"])
                    ),
                    modified_confidentiality_impact=Decimal(
                        str(kwargs["modified_confidentiality_impact"])
                    ),
                    modified_integrity_impact=Decimal(
                        str(kwargs["modified_integrity_impact"])
                    ),
                    modified_privileges_required=Decimal(
                        str(kwargs["modified_privileges_required"])
                    ),
                    modified_severity_scope=Decimal(
                        str(kwargs["modified_severity_scope"])
                    ),
                    modified_user_interaction=Decimal(
                        str(kwargs["modified_user_interaction"])
                    ),
                    privileges_required=Decimal(
                        str(kwargs["privileges_required"])
                    ),
                    remediation_level=Decimal(
                        str(kwargs["remediation_level"])
                    ),
                    report_confidence=Decimal(
                        str(kwargs["report_confidence"])
                    ),
                    severity_scope=Decimal(str(kwargs["severity_scope"])),
                    user_interaction=Decimal(str(kwargs["user_interaction"])),
                ),
                source=requests_utils.get_source_new(info.context),
                threat=threat,
                title=title,
                unfulfilled_requirements=kwargs["unfulfilled_requirements"],
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added finding in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add finding in {group_name} group",
        )
        raise

    return SimplePayload(success=True)
