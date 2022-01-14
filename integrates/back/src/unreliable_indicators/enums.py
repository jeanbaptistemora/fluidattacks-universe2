# pylint: disable=invalid-name
from enum import (
    Enum,
)


class Entity(Enum):
    finding: str = "finding"
    vulnerability: str = "vulnerability"


class EntityId(Enum):
    ids: str = "ids"


class EntityAttr(Enum):
    efficacy: str = "efficacy"
    closed_vulnerabilities: str = "closed_vulnerabilities"
    is_verified: str = "is_verified"
    last_reattack_date: str = "last_reattack_date"
    last_reattack_requester: str = "last_reattack_requester"
    last_requested_reattack_date: str = "last_requested_reattack_date"
    newest_vulnerability_report_date: str = "last_vulnerability_report_date"
    oldest_open_vulnerability_report_date: str = (
        "oldest_open_vulnerability_report_date"
    )
    oldest_vulnerability_report_date: str = "oldest_vulnerability_report_date"
    open_vulnerabilities: str = "open_vulnerabilities"
    reattack_cycles: str = "reattack_cycles"
    status: str = "status"
    treatment_summary: str = "treatment_summary"
    where: str = "where"


class EntityDependency(Enum):
    deactivate_root: str = "deactivate_root"
    handle_vulnerabilities_acceptance: str = (
        "handle_vulnerabilities_acceptance"
    )
    reject_vulnerabilities_zero_risk: str = "reject_vulnerabilities_zero_risk"
    remove_vulnerability: str = "remove_vulnerability"
    request_vulnerabilities_verification: str = (
        "request_vulnerabilities_verification"
    )
    request_vulnerabilities_zero_risk: str = (
        "request_vulnerabilities_zero_risk"
    )
    reset_expired_accepted_findings: str = "reset_expired_accepted_findings"
    update_vulnerabilities_treatment: str = "update_vulnerabilities_treatment"
    update_vulnerability_commit: str = "update_vulnerability_commit"
    upload_file: str = "upload_file"
    verify_vulnerabilities_request: str = "verify_vulnerabilities_request"
