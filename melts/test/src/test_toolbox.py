# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=unused-argument

from toolbox import (
    utils,
)
from typing import (
    Any,
)

# Constants
SUBS: str = "absecon"


def test_toolbox_get_group_from_commit_msg(relocate: Any) -> None:
    """Test toolbox.get_group_from_commit_msg."""
    utils.get_commit_subs.main()
