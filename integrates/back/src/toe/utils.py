from typing import (
    Optional,
)


def get_has_vulnerabilities(
    be_present: bool,
    has_vulnerabilities: Optional[bool],
) -> bool:
    return False if be_present is False else has_vulnerabilities or False
