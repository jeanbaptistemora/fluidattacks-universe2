# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from utils.fs import (
    path_is_include,
    transform_glob,
)


@pytest.mark.skims_test_group("unittesting")
def test_transform_glob() -> None:
    assert transform_glob("glob(**/*.txt)") == "**/*.txt"
    assert transform_glob("*.txt") == "*.txt"
    assert transform_glob("globs(**/*.txt)") == "globs(**/*.txt)"


@pytest.mark.skims_test_group("unittesting")
def test_path_is_include() -> None:
    assert path_is_include(
        "users/danny.txt", include_patterns=["glob(**/*.txt)"]
    )
    assert (
        path_is_include(
            "users/danny.txt",
            include_patterns=["glob(**/*.txt)"],
            exclude_patterns=["users/*.txt"],
        )
        is False
    )
    assert (
        path_is_include(
            "logs/logging.log",
            include_patterns=["assets/"],
            exclude_patterns=["logs/"],
        )
        is False
    )
    assert (
        path_is_include(
            "assets/index.js",
            include_patterns=["assets/"],
            exclude_patterns=["images/"],
        )
        is True
    )
    assert (
        path_is_include(
            "assets/index.min.js",
            include_patterns=["assets/"],
            exclude_patterns=["assets/*.min.js"],
        )
        is False
    )
    assert path_is_include(
        "docs/parts/a.pdf",
        include_patterns=["docs/**/*.pdf"],
        exclude_patterns=["docs/**/*.xls"],
    )

    assert (
        path_is_include(
            "docs/parts/a.xls",
            include_patterns=["docs/**/*.pdf"],
            exclude_patterns=["docs/**/*.xls"],
        )
        is False
    )
    assert (
        path_is_include(
            "images/icon.png",
            include_patterns=["docs/**/*.pdf"],
            exclude_patterns=["docs/**/*.xls"],
        )
        is False
    )
    assert (
        path_is_include(
            "templates/error.html",
            include_patterns=["."],
        )
        is True
    )
