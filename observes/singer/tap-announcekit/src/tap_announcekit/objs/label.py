# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    LabelId,
)

JsonStr = str


@dataclass(frozen=True)
class Label:
    name: str
    color: str


LabelObj = IndexedObj[LabelId, Label]
