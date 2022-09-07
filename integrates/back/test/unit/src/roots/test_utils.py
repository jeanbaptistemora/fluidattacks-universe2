# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from roots import (
    utils as roots_utils,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    "url_input,expected",
    [
        (
            "https://mycompany@dev.azure.com/"
            "mycompany/myproject/_git/myproject",
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
        (
            "https://mycompany@dev.azure.com:30/"
            "mycompany/myproject/_git/myproject",
            "https://dev.azure.com:30/mycompany/myproject/_git/myproject",
        ),
        (
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-universe/demo/demo",
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-universe/demo/demo",
        ),
        (
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
    ],
)
def test_format_url(url_input: str, expected: str) -> None:
    assert roots_utils.format_git_repo_url(url_input) == expected
