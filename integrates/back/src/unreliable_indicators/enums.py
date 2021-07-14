from enum import (
    Enum,
)


class EntityName(Enum):
    finding: str = "finding"


class EntityIdName(Enum):
    id: str = "id"


class EntityAttrName(Enum):
    unreliable_age: str = "unreliable_age"
    unreliable_closed_vulnerabilities: str = (
        "unreliable_closed_vulnerabilities"
    )
    unreliable_is_verified: str = "unreliable_is_verified"
    unreliable_last_vulnerability: str = "unreliable_last_vulnerability"
    unreliable_open_age: str = "unreliable_open_age"
    unreliable_open_vulnerabilities: str = "unreliable_open_vulnerabilities"
    unreliable_report_date: str = "unreliable_report_date"
    unreliable_status: str = "unreliable_status"
