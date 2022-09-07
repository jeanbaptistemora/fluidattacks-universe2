# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .root import (
    ROOT,
)
from ariadne import (
    UnionType,
)
from typing import (
    Tuple,
)

UNIONS: Tuple[UnionType, ...] = (ROOT,)
