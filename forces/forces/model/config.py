# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from io import (
    TextIOWrapper,
)
from typing import (
    NamedTuple,
)


class KindEnum(str, Enum):
    """DAST / SAST vulnerabilities mode"""

    ALL: str = "all"
    DYNAMIC: str = "dynamic"
    STATIC: str = "static"


class ForcesConfig(NamedTuple):
    """Forces user config"""

    group: str
    kind: KindEnum = KindEnum.ALL
    output: TextIOWrapper | None = None
    repository_path: str | None = "."
    repository_name: str | None = None
    strict: bool | None = False
    verbose_level: int = 3
    breaking_severity: float = 0.0
    grace_period: int = 0
