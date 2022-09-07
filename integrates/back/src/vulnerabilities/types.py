# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class GroupedVulnerabilitiesInfo(NamedTuple):
    commit_hash: Optional[str]
    specific: str
    where: str


class FindingGroupedVulnerabilitiesInfo(NamedTuple):
    grouped_ports_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_inputs_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    where: str


class Treatments(NamedTuple):
    accepted: int
    accepted_undefined: int
    in_progress: int
    new: int


class Verifications(NamedTuple):
    requested: int
    on_hold: int
    verified: int


ToolItem = dict[str, str]
