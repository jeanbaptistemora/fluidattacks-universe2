
from datetime import datetime
from decimal import Decimal
from typing import Union

from model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
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


def get_updated_evidence_date_new(
    finding: Finding,
    evidence: FindingEvidence
) -> datetime:
    evidence_date = datetime.fromisoformat(evidence.modified_date)
    updated_date = evidence_date
    if finding.approval:
        release_date = datetime.fromisoformat(
            finding.approval.modified_date
        )
        if release_date > evidence_date:
            updated_date = release_date
    return updated_date
