from .payloads.types import (
    SimpleFindingPayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidCvssField,
    InvalidCvssVersion,
    NotCvssVersion,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.enums import (
    FindingCvssVersion,
)
from db_model.findings.types import (
    Finding20Severity,
    Finding31Severity,
)
from decimal import (
    Decimal,
    InvalidOperation,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    validations,
)
from typing import (
    Any,
)


@MUTATION.field("updateSeverity")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, finding_id: str, **kwargs: Any
) -> SimpleFindingPayload:
    try:
        loaders: Dataloaders = info.context.loaders
        kwargs["id"] = finding_id
        finding = await findings_domain.get_finding(loaders, finding_id)
        if "cvss_version" not in kwargs:
            raise NotCvssVersion()
        cvss_version = str(kwargs["cvss_version"])
        try:
            cvss_fields = {
                key: Decimal(str(value))
                for key, value in kwargs.items()
                if key not in {"cvss_version", "id"}
            }
        except InvalidOperation as ex:
            raise InvalidCvssField() from ex
        validations.validate_missing_severity_field_names(
            set(cvss_fields.keys()), cvss_version
        )
        validations.validate_update_severity_values(cvss_fields)
        severity: Finding20Severity | Finding31Severity
        if cvss_version == FindingCvssVersion.V20.value:
            severity = Finding20Severity(
                access_complexity=cvss_fields["access_complexity"],
                access_vector=cvss_fields["access_vector"],
                authentication=cvss_fields["authentication"],
                availability_impact=cvss_fields["availability_impact"],
                availability_requirement=cvss_fields[
                    "availability_requirement"
                ],
                collateral_damage_potential=cvss_fields[
                    "collateral_damage_potential"
                ],
                confidence_level=cvss_fields["confidence_level"],
                confidentiality_impact=cvss_fields["confidentiality_impact"],
                confidentiality_requirement=cvss_fields[
                    "confidentiality_requirement"
                ],
                exploitability=cvss_fields["exploitability"],
                finding_distribution=cvss_fields["finding_distribution"],
                integrity_impact=cvss_fields["integrity_impact"],
                integrity_requirement=cvss_fields["integrity_requirement"],
                resolution_level=cvss_fields["resolution_level"],
            )
        elif cvss_version == FindingCvssVersion.V31.value:
            severity = Finding31Severity(
                attack_complexity=cvss_fields["attack_complexity"],
                attack_vector=cvss_fields["attack_vector"],
                availability_impact=cvss_fields["availability_impact"],
                availability_requirement=cvss_fields[
                    "availability_requirement"
                ],
                confidentiality_impact=cvss_fields["confidentiality_impact"],
                confidentiality_requirement=cvss_fields[
                    "confidentiality_requirement"
                ],
                exploitability=cvss_fields["exploitability"],
                integrity_impact=cvss_fields["integrity_impact"],
                integrity_requirement=cvss_fields["integrity_requirement"],
                modified_attack_complexity=cvss_fields[
                    "modified_attack_complexity"
                ],
                modified_attack_vector=cvss_fields["modified_attack_vector"],
                modified_availability_impact=cvss_fields[
                    "modified_availability_impact"
                ],
                modified_confidentiality_impact=cvss_fields[
                    "modified_confidentiality_impact"
                ],
                modified_integrity_impact=cvss_fields[
                    "modified_integrity_impact"
                ],
                modified_privileges_required=cvss_fields[
                    "modified_privileges_required"
                ],
                modified_user_interaction=cvss_fields[
                    "modified_user_interaction"
                ],
                modified_severity_scope=cvss_fields["modified_severity_scope"],
                privileges_required=cvss_fields["privileges_required"],
                remediation_level=cvss_fields["remediation_level"],
                report_confidence=cvss_fields["report_confidence"],
                severity_scope=cvss_fields["severity_scope"],
                user_interaction=cvss_fields["user_interaction"],
            )
        else:
            raise InvalidCvssVersion()

        await findings_domain.update_severity(loaders, finding_id, severity)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated severity in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update severity in finding {finding_id}",
        )
        raise

    loaders.finding.clear(finding_id)
    finding = await findings_domain.get_finding(loaders, finding_id)

    return SimpleFindingPayload(finding=finding, success=True)
