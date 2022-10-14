# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_ID = TypeVar("_ID")
_T = TypeVar("_T")


@dataclass(frozen=True)
class IndexedObj(Generic[_ID, _T]):
    id_obj: _ID
    obj: _T
