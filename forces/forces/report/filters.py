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


def filter_kind(
    vuln: Vulnerability,
    kind: KindEnum,
) -> bool:
    return (
        (kind == KindEnum.DYNAMIC and vuln.type == VulnerabilityType.DAST)
        or (kind == KindEnum.STATIC and vuln.type == VulnerabilityType.SAST)
        or kind == KindEnum.ALL
    )


def filter_repo(
    vuln: Vulnerability,
    kind: KindEnum,
    repo_name: str | None = None,
) -> bool:
    if (
        kind in (KindEnum.ALL, KindEnum.STATIC)
        and vuln.type == VulnerabilityType.SAST
        and repo_name
    ):
        return fnmatch.fnmatch(vuln.where, f"{repo_name}/*")
    if (
        kind in (KindEnum.ALL, KindEnum.DYNAMIC)
        and vuln.type == VulnerabilityType.DAST
    ):
        return vuln.root_nickname == repo_name or not vuln.root_nickname
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
