# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# flake8: noqa

import textwrap
from toolbox.utils.generic import (
    get_change_request_body,
    get_change_request_deltas,
    get_change_request_hunks,
    get_change_request_patch,
    get_change_request_summary,
)


def test_get_change_request_summary() -> None:
    assert "fix" in get_change_request_summary("45531778")


def test_get_change_request_body() -> None:
    expected: str = "- updated config\n"
    assert get_change_request_body("c2848e0b0") == expected


def test_get_change_request_patch_and_hunks() -> None:
    expected: str = textwrap.dedent(
        """
        diff --git a/.gitignore b/.gitignore
        new file mode 100644
        index 000000000..8c388a265
        --- /dev/null
        +++ b/.gitignore
        @@ -0,0 +1,6 @@
        +# Add any directories, files, or patterns you don't want to be tracked by version control
        +**/fusion/*
        +**/reports/*
        +
        +# FLUID concurrent
        +build/
        """[
            1:
        ]
    )[:-1]

    assert get_change_request_patch("44c9195") == expected
    assert get_change_request_hunks("44c9195") == [expected + "\n"]


def test_get_change_request_deltas() -> None:
    assert get_change_request_deltas("caf6a78") == 33
