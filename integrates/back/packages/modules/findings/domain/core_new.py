from decimal import Decimal
from typing import Union

from model.findings.types import (
    Finding20Severity,
    Finding31Severity
)
from newutils import cvss_new


def get_severity_score_new(
    severity: Union[Finding20Severity, Finding31Severity]
) -> Decimal:
    if isinstance(severity, Finding31Severity):
        base_score = cvss_new.get_cvss3_basescore(severity)
        cvss_temporal = cvss_new.get_cvss3_temporal(severity, base_score)
    else:
        base_score = cvss_new.get_cvss2_basescore(severity)
        cvss_temporal = cvss_new.get_cvss2_temporal(severity, base_score)
    return cvss_temporal
