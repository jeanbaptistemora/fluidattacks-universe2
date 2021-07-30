from enum import (
    Enum,
)


class Entity(Enum):
    finding: str = "finding"


class EntityId(Enum):
    id: str = "id"


class EntityAttr(Enum):
    age: str = "age"
    closed_vulnerabilities: str = "closed_vulnerabilities"
    is_verified: str = "is_verified"
    last_vulnerability: str = "last_vulnerability"
    open_age: str = "open_age"
    open_vulnerabilities: str = "open_vulnerabilities"
    report_date: str = "report_date"
    status: str = "status"


class EntityDependency(Enum):
    reject_zero_risk_vuln: str = "reject_vulnerabilities_zero_risk"
    remove_vulnerability: str = "remove_vulnerability"
    request_verification_vulnerability: str = (
        "request_vulnerabilities_verification"
    )
    request_zero_risk_vuln: str = "request_vulnerabilities_zero_risk"
    upload_file: str = "upload_file"
    verify_request_vulnerability: str = "verify_vulnerabilities_request"
