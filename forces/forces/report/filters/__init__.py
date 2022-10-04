# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import fnmatch
from forces.model.config import (
    KindEnum,
)
from forces.model.vulnerability import (
    VulnerabilityType,
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
    vuln_type = (
        VulnerabilityType.SAST
        if vuln["vulnerabilityType"] == "lines"
        else VulnerabilityType.DAST
    )
    return (
        (kind == KindEnum.DYNAMIC and vuln_type == VulnerabilityType.DAST)
        or (kind == KindEnum.STATIC and vuln_type == VulnerabilityType.SAST)
        or kind == KindEnum.ALL
    )


def filter_repo(
    vuln: Dict[str, Any],
    kind: KindEnum,
    repo_name: Optional[str] = None,
) -> bool:
    vuln_type: VulnerabilityType = (
        VulnerabilityType.SAST
        if vuln["vulnerabilityType"] == "lines"
        else VulnerabilityType.DAST
    )

    if (
        kind in (KindEnum.ALL, KindEnum.STATIC)
        and vuln_type == VulnerabilityType.SAST
        and repo_name
    ):
        return fnmatch.fnmatch(cast(str, vuln["where"]), f"{repo_name}/*")
    if (
        kind in (KindEnum.ALL, KindEnum.DYNAMIC)
        and vuln_type == VulnerabilityType.DAST
    ):
        root_nickname: Optional[str] = vuln.get("rootNickname", "")
        return root_nickname == repo_name or not root_nickname
    return True
