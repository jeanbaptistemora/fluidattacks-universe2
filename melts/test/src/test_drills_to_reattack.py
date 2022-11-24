# pylint: disable=unused-argument

from toolbox.drills.to_reattack import (
    to_reattack,
)
from typing import (
    Any,
)

# Constants
GROUP: str = "absecon"


def test_drills_to_reattack(relocate: Any) -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    data: list = to_reattack(GROUP)["groups_info"]

    assert data[0]["name"] == GROUP
    assert data[0]["findings"][0]["url"] == (
        f"https://app.fluidattacks.com/groups/{GROUP}/vulns/677264467"
    )
    assert len(data[0]["findings"][0]["vulnerabilities"]) == 1
