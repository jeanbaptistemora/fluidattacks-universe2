# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.iam.utils import (
    match_pattern,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_match_pattern() -> None:
    base_pattern: str = "iam:PassRole"
    assert match_pattern(base_pattern, base_pattern)
    assert match_pattern("iam:PassR*", base_pattern)
    assert match_pattern("iam:Pass*", base_pattern)
    assert match_pattern("iam:P*", base_pattern)
    assert match_pattern("iam:*PassRole", base_pattern)
    assert match_pattern("iam:*PassR*", base_pattern)
    assert match_pattern("iam:*Pass*", base_pattern)
    assert match_pattern("iam:*P*", base_pattern)
    assert match_pattern("iam:*", base_pattern)
    assert match_pattern("iam*", base_pattern)
    assert match_pattern("*:PassRole", base_pattern)
    assert match_pattern("*:*Pass*", base_pattern)
    assert match_pattern("*", base_pattern)
    assert match_pattern(".*", ".iam:PassRole")

    assert not match_pattern("a*", base_pattern)
    assert not match_pattern("iam", base_pattern)
    assert not match_pattern("iam:PassRol", base_pattern)

    # Ensure symbolic chars in a regex context are properly escaped
    assert not match_pattern(".", "x")
    assert not match_pattern("iam:PassRol.", base_pattern)
    assert not match_pattern("iam:Pa.sRol.", base_pattern)
    assert not match_pattern("............", base_pattern)
    assert not match_pattern(".*", base_pattern)
