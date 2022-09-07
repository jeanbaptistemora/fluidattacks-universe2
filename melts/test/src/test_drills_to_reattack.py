# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=unused-argument

import pytest
from toolbox.drills.to_reattack import (
    to_reattack,
)
from typing import (
    Any,
)


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_drills_to_reattack(relocate: Any) -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    data: list = to_reattack("continuoustest")["projects_info"]

    assert data[0]["name"] == "continuoustest"
    assert data[0]["findings"][0]["url"] == (
        "https://app.fluidattacks.com/groups/continuoustest/vulns/508273958"
    )
    assert len(data[0]["findings"][0]["vulnerabilities"]) == 2
