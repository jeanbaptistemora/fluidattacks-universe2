# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import fnmatch
from forces.model import (
    KindEnum,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from typing import (
    Any,
    cast,
)


def filter_kind(
    vuln: dict[str, Any],
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
    vuln: dict[str, Any],
    kind: KindEnum,
    repo_name: str | None = None,
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
        root_nickname: str | None = vuln.get("rootNickname", "")
        return root_nickname == repo_name or not root_nickname
    return True


def filter_vulnerabilities(
    vulnerabilities: list[Vulnerability],
    verbose_level: int,
) -> tuple[Vulnerability, ...]:
    """Helper method to filter vulns in findings based on the requested vuln
    states set by the verbosity level of the report"""
    verbosity: dict[int, set[VulnerabilityState]] = {
        1: set(),
        2: {VulnerabilityState.OPEN},
        3: {VulnerabilityState.OPEN, VulnerabilityState.CLOSED},
        4: set(VulnerabilityState),
    }
    return (
        tuple(
            filter(
                lambda vuln: vuln.state in verbosity[verbose_level],
                vulnerabilities,
            )
        )
        if verbose_level != 1
        else tuple()
    )
