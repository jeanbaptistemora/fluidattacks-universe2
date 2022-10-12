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
from lib_path.f393.gem import (
    gem_gemfile_dev,
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
    Tuple,
)


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"
    gemfile_dep: Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    gem_gemfile_fun = gem_gemfile.__wrapped__  # type: ignore
    content: List[str] = file_contents.splitlines()
    generator_gem: Iterator[DependencyType] = gem_gemfile_fun(
        file_contents, path
    )
    assertion: bool = True
    lines_prod_deps = [*range(116), 130, 133, 136, 139, *range(148, 182)]
    for line_num in lines_prod_deps:
        if matched := re.search(gemfile_dep, content[line_num]):
            pkg_name: str = matched.group("name")

            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_name == item and line_num + 1 == line
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_lock() -> None:
    gem_lock_dep: Pattern[str] = re.compile(
        r"(?P<gem>(?P<name>[\w\-]+)\s?(\(.*\))?)"
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
            gem_info: str = matched.group("gem").replace("(= ", "(")
            if gem_info in pkg_names_arr:
                continue
            pkg_names_arr.append(gem_info)
            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            if pkg_name != item or line_num + 1 != line:
                assertion = not assertion
                break

    assert assertion


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
        ("minitest-ci", "", 119),
        ("minitest-retry", "", 120),
        ("stackprof", "=1.4.2", 123),
        ("debug", ">=1.1.0", 124),
        ("benchmark-ips", "", 127),
        ("devise", "=1.4.2", 132),
        ("rubocop", "=1.35.1", 133),
        ("pg", "^1.3", 143),
        ("mysql2", "^0.5", 144),
        ("pry", "=1.0.1", 145),
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
