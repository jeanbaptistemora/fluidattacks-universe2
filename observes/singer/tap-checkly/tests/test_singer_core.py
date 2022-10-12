# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from tap_checkly.singer import (
    SingerStreams,
)


def test_unique() -> None:
    assert iter(SingerStreams)
