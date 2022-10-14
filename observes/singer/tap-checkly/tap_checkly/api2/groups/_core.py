# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from tap_checkly.objs import (
    CheckGroup,
    CheckGroupId,
    IndexedObj,
)

CheckGroupObj = IndexedObj[CheckGroupId, CheckGroup]


__all__ = [
    "CheckGroupId",
    "CheckGroup",
]
