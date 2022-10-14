# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from tap_checkly.objs import (
    Check,
    CheckConf1,
    CheckConf2,
    CheckId,
    IndexedObj,
)

CheckObj = IndexedObj[CheckId, Check]
__all__ = [
    "CheckConf1",
    "CheckConf2",
    "Check",
    "CheckId",
]
