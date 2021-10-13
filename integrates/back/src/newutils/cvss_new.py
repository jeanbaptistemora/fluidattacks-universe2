from db_model.findings.types import (
    Finding20CvssParameters,
    Finding20Severity,
    Finding31CvssParameters,
    Finding31Severity,
)
from decimal import (
    Decimal,
)
import math

DEFAULT_20_CVSS_PARAMETERS = Finding20CvssParameters(
    bs_factor_1=Decimal("0.6"),
    bs_factor_2=Decimal("0.4"),
    bs_factor_3=Decimal("1.5"),
    impact_factor=Decimal("10.41"),
    exploitability_factor=Decimal("20"),
)
DEFAULT_31_CVSS_PARAMETERS = Finding31CvssParameters(
    basescore_factor=Decimal("1.08"),
    exploitability_factor_1=Decimal("8.22"),
    impact_factor_1=Decimal("6.42"),
    impact_factor_2=Decimal("7.52"),
    impact_factor_3=Decimal("0.029"),
    impact_factor_4=Decimal("3.25"),
    impact_factor_5=Decimal("0.02"),
    impact_factor_6=Decimal("15"),
    mod_impact_factor_1=Decimal("0.915"),
    mod_impact_factor_2=Decimal("6.42"),
    mod_impact_factor_3=Decimal("7.52"),
    mod_impact_factor_4=Decimal("0.029"),
    mod_impact_factor_5=Decimal("3.25"),
    mod_impact_factor_6=Decimal("0.02"),
    mod_impact_factor_7=Decimal("13"),
    mod_impact_factor_8=Decimal("0.9731"),
)


def get_f_impact(impact: Decimal) -> Decimal:
    if impact:
        f_impact_factor = Decimal("1.176")
    else:
        f_impact_factor = Decimal("0.0")
    return f_impact_factor


def get_cvss3_basescore(
    severity: Finding31Severity,
    parameters: Finding31CvssParameters = DEFAULT_31_CVSS_PARAMETERS,
) -> Decimal:
    """Calculate cvss 3.1 base score attribute."""
    iss = 1 - (
        (1 - severity.confidentiality_impact)
        * (1 - severity.integrity_impact)
        * (1 - severity.availability_impact)
    )
    if severity.severity_scope:
        impact = (
            parameters.impact_factor_2 * (iss - parameters.impact_factor_3)
        ) - (
            parameters.impact_factor_4
            * (iss - parameters.impact_factor_5) ** parameters.impact_factor_6
        )
    else:
        impact = parameters.impact_factor_1 * iss
    exploitability = (
        parameters.exploitability_factor_1
        * severity.attack_vector
        * severity.attack_complexity
        * severity.privileges_required
        * severity.user_interaction
    )
    if impact <= 0:
        basescore = Decimal(0)
    else:
        if severity.severity_scope:
            basescore = Decimal(
                math.ceil(
                    min(
                        (
                            parameters.basescore_factor
                            * (impact + exploitability)
                        ),
                        10,
                    )
                    * 10
                )
                / 10
            )
        else:
            basescore = Decimal(
                math.ceil(min(impact + exploitability, 10) * 10) / 10
            )
    resp = basescore.quantize(Decimal("0.1"))
    return resp


def get_cvss3_temporal(
    severity: Finding31Severity, basescore: Decimal
) -> Decimal:
    """Calculate cvss 3.1 temporal attribute."""
    temporal = Decimal(
        math.ceil(
            basescore
            * severity.exploitability
            * severity.remediation_level
            * severity.report_confidence
            * 10
        )
        / 10
    )
    resp = temporal.quantize(Decimal("0.1"))
    return resp


def get_cvss2_basescore(
    severity: Finding20Severity,
    parameters: Finding20CvssParameters = DEFAULT_20_CVSS_PARAMETERS,
) -> Decimal:
    """Calculate cvss 2.0 base score attribute."""
    impact = parameters.impact_factor * (
        1
        - (
            (1 - severity.confidentiality_impact)
            * (1 - severity.integrity_impact)
            * (1 - severity.availability_impact)
        )
    )
    f_impact_factor = get_f_impact(impact)
    exploitabilty = (
        parameters.exploitability_factor
        * severity.access_complexity
        * severity.authentication
        * severity.access_vector
    )
    basescore = Decimal(
        (
            parameters.bs_factor_1 * impact
            - parameters.bs_factor_3
            + parameters.bs_factor_2 * exploitabilty
        )
        * f_impact_factor
    )
    resp = basescore.quantize(Decimal("0.1"))
    return resp


def get_cvss2_temporal(
    severity: Finding20Severity, basescore: Decimal
) -> Decimal:
    """Calculate cvss 2.0 temporal attribute."""
    temporal = Decimal(
        basescore
        * severity.exploitability
        * severity.exploitability
        * severity.confidence_level
    )
    resp = temporal.quantize(Decimal("0.1"))
    return resp


def calculate_privileges(privileges: float, scope: float) -> float:
    """Calculate privileges attribute."""
    if scope:
        if privileges == 0.62:
            privileges = 0.68
        elif privileges == 0.27:
            privileges = 0.5
    else:
        if privileges == 0.68:
            privileges = 0.62
        elif privileges == 0.5:
            privileges = 0.27

    return privileges
