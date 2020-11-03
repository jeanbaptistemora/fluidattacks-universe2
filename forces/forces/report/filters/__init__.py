# Standard imports
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)
import fnmatch


def filter_kind(
    vuln: Dict[str, Any],
    kind: str,
) -> bool:
    vuln_type = 'SAST' if vuln['vulnType'] == 'lines' else 'DAST'
    return (kind == 'dynamic' and vuln_type == 'DAST') or (
        kind == 'static' and vuln_type == 'SAST') or kind == 'all'


def filter_repo(
    vuln: Dict[str, Any],
    kind: str,
    repo_name: Optional[str],
) -> bool:
    vuln_type = 'SAST' if vuln['vulnType'] == 'lines' else 'DAST'

    if kind in ('all', 'static') and vuln_type == 'SAST' and repo_name:
        return fnmatch.fnmatch(cast(str, vuln['where']), f"{repo_name}/*")
    return True
