from enum import (
    Enum,
)


class EntityName(Enum):
    finding: str = "finding"


class EntityIdName(Enum):
    id: str = "id"


class EntityAttrName(Enum):
    age: str = "age"
    closed_vulnerabilities: str = "closed_vulnerabilities"
    is_verified: str = "is_verified"
    last_vulnerability: str = "last_vulnerability"
    open_age: str = "open_age"
    open_vulnerabilities: str = "open_vulnerabilities"
    report_date: str = "report_date"
    status: str = "status"
