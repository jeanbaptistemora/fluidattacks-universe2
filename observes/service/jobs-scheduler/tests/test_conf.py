# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from jobs_scheduler.conf.schedule import (
    SCHEDULE,
)


def test_schedule() -> None:
    assert SCHEDULE
