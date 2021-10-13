from db_model.findings.types import (
    Finding20Severity,
    Finding31Severity,
)
from decimal import (
    Decimal,
)
from newutils import (
    cvss_new,
    utils,
)
from typing import (
    Dict,
)


def format_severity(severity: Dict[str, float]) -> Dict[str, Decimal]:
    return {
        utils.camelcase_to_snakecase(key): Decimal(value)
        for key, value in severity.items()
    }


def test_calculate_cvss2_basescore() -> None:
    severity = {
        "confidentialityImpact": 0,
        "integrityImpact": 0.275,
        "availabilityImpact": 0,
        "accessComplexity": 0.61,
        "authentication": 0.704,
        "accessVector": 1,
    }
    cvss_basescore_test = Decimal(4.3).quantize(Decimal("0.1"))
    severity_new = Finding20Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss2_basescore(severity_new)
    assert cvss_basescore_new == cvss_basescore_test


def test_calculate_cvss2_temporal() -> None:
    severity = {
        "confidentialityImpact": 0,
        "integrityImpact": 0.275,
        "availabilityImpact": 0,
        "accessComplexity": 0.61,
        "authentication": 0.704,
        "accessVector": 1,
        "exploitability": 0.95,
        "resolutionLevel": 0.95,
        "confidenceLevel": 0.95,
    }
    cvss_temporal_test = Decimal(3.7).quantize(Decimal("0.1"))
    severity_new = Finding20Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss2_basescore(severity_new)
    cvss_temporal_new = cvss_new.get_cvss2_temporal(
        severity_new, cvss_basescore_new
    )
    assert cvss_temporal_new == cvss_temporal_test


def test_calculate_cvss3_scope_changed_basescore() -> None:
    severity = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 1,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.68,
        "userInteraction": 0.85,
    }
    cvss_basescore_test = Decimal(6.4).quantize(Decimal("0.1"))
    severity_new = Finding31Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss3_basescore(severity_new)
    assert cvss_basescore_new == cvss_basescore_test


def test_calculate_cvss3_scope_unchanged_basescore() -> None:
    severity = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 0,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.62,
        "userInteraction": 0.85,
    }
    cvss_basescore_test = Decimal(5.4).quantize(Decimal("0.1"))
    severity_new = Finding31Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss3_basescore(severity_new)
    assert cvss_basescore_new == cvss_basescore_test


def test_calculate_cvss3_scope_changed_temporal() -> None:
    severity = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 1,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.68,
        "userInteraction": 0.85,
        "exploitability": 0.97,
        "remediationLevel": 0.97,
        "reportConfidence": 1,
    }
    cvss_temporal_test = Decimal(6.1).quantize(Decimal("0.1"))
    severity_new = Finding31Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss3_basescore(severity_new)
    cvss_temporal_new = cvss_new.get_cvss3_temporal(
        severity_new, cvss_basescore_new
    )
    assert cvss_temporal_new == cvss_temporal_test


def test_calculate_cvss3_scope_unchanged_temporal() -> None:
    severity = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 0,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.62,
        "userInteraction": 0.85,
        "exploitability": 0.97,
        "remediationLevel": 0.97,
        "reportConfidence": 1,
    }
    cvss_temporal_test = Decimal(5.1).quantize(Decimal("0.1"))
    severity_new = Finding31Severity(**format_severity(severity))
    cvss_basescore_new = cvss_new.get_cvss3_basescore(severity_new)
    cvss_temporal_new = cvss_new.get_cvss3_temporal(
        severity_new, cvss_basescore_new
    )
    assert cvss_temporal_new == cvss_temporal_test
