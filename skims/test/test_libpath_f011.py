# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    DependencyType,
)
from lib_path.f011.gem import (
    gem_gemfile,
    gem_gemfile_lock,
)
from operator import (
    itemgetter,
)
import pytest
import re
from typing import (
    Iterator,
    List,
    Pattern,
)


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"

    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
        gem_gemfile_unwrapped = gem_gemfile.__wrapped__  # type: ignore

    expected = (
        (
            {"column": 0, "line": 27, "item": "puma"},
            {"column": 0, "line": 27, "item": "5.1.0"},
        ),
        (
            {"column": 0, "line": 28, "item": "rdoc"},
            {"column": 0, "line": 28, "item": "3.11"},
        ),
        (
            {"column": 0, "line": 131, "item": "nokogiri"},
            {"column": 0, "line": 131, "item": "1.8.1"},
        ),
        (
            {"column": 0, "line": 134, "item": "rails"},
            {"column": 0, "line": 134, "item": "7.0.4"},
        ),
        (
            {"column": 0, "line": 175, "item": "mini_magick"},
            {"column": 0, "line": 175, "item": "4.9.0"},
        ),
    )
    assert tuple(gem_gemfile_unwrapped(file_contents, path)) == expected


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_lock() -> None:
    gem_lock_dep: Pattern[str] = re.compile(
        r"(?P<name>[\w\-]+)\s\(=?\s?(?P<version>(\d{1,2}\.?){2,4})"
    )
    path: str = "skims/test/data/lib_path/f011/Gemfile.lock"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
        content: List[str] = file_contents.splitlines()
        gemfile_lock_fun = gem_gemfile_lock.__wrapped__  # type: ignore
        generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
            file_contents, path
        )
        pkg_names_arr: List[str] = []
        assertion: bool = True

        for line_num in range(22, 219):
            if matched := re.search(gem_lock_dep, content[line_num]):
                pkg_name: str = matched.group("name")
                if pkg_name in pkg_names_arr:
                    continue
                pkg_names_arr.append(pkg_name)
                try:
                    line, item = itemgetter("line", "item")(
                        next(generator_gem)[0]
                    )
                except StopIteration:
                    assertion = not assertion
                    break
                equal_props: bool = pkg_name == item and line_num + 1 == line
                if not equal_props:
                    assertion = not assertion
                    break

        assert assertion
