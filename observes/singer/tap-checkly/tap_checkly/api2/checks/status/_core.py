# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from tap_checkly.objs import (
    CheckId,
    CheckStatus,
    IndexedObj,
)

CheckStatusObj = IndexedObj[CheckId, CheckStatus]
__all__ = [
    "CheckId",
    "CheckStatus",
]
