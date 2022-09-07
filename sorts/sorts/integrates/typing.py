# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class Vulnerability(NamedTuple):  # pylint: disable=too-few-public-methods
    kind: VulnerabilityKindEnum
    title: str
    where: str


class ToeLines(NamedTuple):  # pylint: disable=too-few-public-methods
    attacked_lines: int
    filename: str
    loc: int
    root_nickname: str
    sorts_risk_level: str
