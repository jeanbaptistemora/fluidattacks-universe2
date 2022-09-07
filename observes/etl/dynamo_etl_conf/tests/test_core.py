# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamo_etl_conf.core import (
    SEGMENTATION,
    TargetTables,
)


def test_completeness() -> None:
    for t in TargetTables:
        assert SEGMENTATION[t]
