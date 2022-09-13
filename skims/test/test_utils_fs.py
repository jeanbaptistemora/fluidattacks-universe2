# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from utils.fs import (
    transform_glob,
)


@pytest.mark.skims_test_group("unittesting")
def test_transform_glob() -> None:
    assert transform_glob("glob(**/*.txt)") == "**/*.txt"
    assert transform_glob("*.txt") == "*.txt"
    assert transform_glob("globs(**/*.txt)") == "globs(**/*.txt)"
