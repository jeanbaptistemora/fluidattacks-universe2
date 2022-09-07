# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from tap_gitlab import (
    __version__,
)


def test_version() -> None:
    assert __version__ == "0.1.0"
