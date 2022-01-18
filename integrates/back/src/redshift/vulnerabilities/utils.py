from db_model.vulnerabilities.types import (
    Vulnerability,
)
from typing import (
    Any,
    Dict,
)


def format_vulnerability_metadata(
    vulnerability: Vulnerability,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability.id,
        custom_severity=vulnerability.custom_severity,
        finding_id=vulnerability.finding_id,
        skims_method=vulnerability.skims_method,
        type=vulnerability.type.value,
    )
