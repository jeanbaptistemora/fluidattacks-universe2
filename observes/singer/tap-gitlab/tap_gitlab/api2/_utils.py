# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    Result,
    ResultE,
)


def int_to_str(num: int) -> str:
    return str(num)


def str_to_datetime(raw: str) -> ResultE[datetime]:
    try:
        return Result.success(isoparse(raw))
    except ValueError as err:
        return Result.failure(err)
