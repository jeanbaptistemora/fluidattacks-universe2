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
    Optional,
)


class KindEnum(Enum):
    """DAST / SAST vulnerabilities mode"""

    ALL: str = "all"
    DYNAMIC: str = "dynamic"
    STATIC: str = "static"


class ForcesConfig(NamedTuple):
    """Forces user config"""

    group: str
    kind: KindEnum = KindEnum.ALL
    output: Optional[TextIOWrapper] = None
    repository_path: Optional[str] = "."
    repository_name: Optional[str] = None
    strict: Optional[bool] = False
    verbose_level: int = 3
    breaking_severity: float = 0.0
    grace_period: int = 0
