# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import fnmatch
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)


def filter_kind(
    vuln: Dict[str, Any],
    kind: str,
) -> bool:
    vuln_type = "SAST" if vuln["vulnerabilityType"] == "lines" else "DAST"
    return (
        (kind == "dynamic" and vuln_type == "DAST")
        or (kind == "static" and vuln_type == "SAST")
        or kind == "all"
    )


def filter_repo(
    vuln: Dict[str, Any],
    kind: str,
    repo_name: Optional[str] = None,
) -> bool:
    vuln_type = "SAST" if vuln["vulnerabilityType"] == "lines" else "DAST"

    if kind in ("all", "static") and vuln_type == "SAST" and repo_name:
        return fnmatch.fnmatch(cast(str, vuln["where"]), f"{repo_name}/*")
    if kind in ("all", "dynamic") and vuln_type == "DAST":
        root_nickname: Optional[str] = vuln.get("rootNickname", "")
        return root_nickname == repo_name or not root_nickname
    return True
