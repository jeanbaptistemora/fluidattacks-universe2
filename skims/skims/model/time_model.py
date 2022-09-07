# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# The purpose of this module is to return datetime AWARE objects
# so the entire codebase work in UTC-based clocks no matter the data-source
from datetime import (
    datetime,
    timedelta,
    timezone,
)

INTEGRATES_1: str = "%Y-%m-%d %H:%M:%S"


def _make_aware(
    naive: datetime,
    *,
    offset: timedelta,
) -> datetime:
    return naive.replace(tzinfo=timezone(offset=offset))


def from_colombian(string: str, fmt: str) -> datetime:
    naive = datetime.strptime(string, fmt)
    return _make_aware(naive, offset=timedelta(hours=-5.0))


def min_posible() -> datetime:
    naive = datetime.utcfromtimestamp(0)
    return _make_aware(naive, offset=timedelta(seconds=0.0))
