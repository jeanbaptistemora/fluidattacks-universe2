# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    DependencyType,
)
from lib_path.f393.gem import (
    gem_gemfile_dev,
)
import pytest
from typing import (
    Iterator,
    Tuple,
)


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"

    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
        gem_gemfile_unwrapped = gem_gemfile_dev.__wrapped__  # type: ignore

    expected: Tuple[Tuple[str, str, int], ...] = (
        ("minitest-bisect", "1.0.0", 118),
        ("stackprof", "1.4.2", 123),
        ("devise", "1.4.2", 132),
        ("rubocop", "1.35.1", 133),
        ("pry", "1.0.1", 145),
    )
    reports: Iterator[DependencyType] = gem_gemfile_unwrapped(
        file_contents, path
    )
    assertion: bool = True
    for num, report in enumerate(reports):
        product = report[0].get("item")
        line = report[0].get("line")
        version = report[1].get("item")
        if (product, version, line) != expected[num]:
            assertion = not assertion
            break

    assert assertion
