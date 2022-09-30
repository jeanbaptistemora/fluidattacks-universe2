# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import fnmatch
from forces.model.config import (
    KindEnum,
)
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)


def filter_kind(
    vuln: Dict[str, Any],
    kind: KindEnum,
) -> bool:
    vuln_type = "SAST" if vuln["vulnerabilityType"] == "lines" else "DAST"
    return (
        (kind == KindEnum.DYNAMIC and vuln_type == "DAST")
        or (kind == KindEnum.STATIC and vuln_type == "SAST")
        or kind == KindEnum.ALL
    )


def filter_repo(
    vuln: Dict[str, Any],
    kind: KindEnum,
    repo_name: Optional[str] = None,
) -> bool:
    vuln_type = "SAST" if vuln["vulnerabilityType"] == "lines" else "DAST"

    if (
        kind in (KindEnum.ALL, KindEnum.STATIC)
        and vuln_type == "SAST"
        and repo_name
    ):
        return fnmatch.fnmatch(cast(str, vuln["where"]), f"{repo_name}/*")
    if kind in (KindEnum.ALL, KindEnum.DYNAMIC) and vuln_type == "DAST":
        root_nickname: Optional[str] = vuln.get("rootNickname", "")
        return root_nickname == repo_name or not root_nickname
    return True
