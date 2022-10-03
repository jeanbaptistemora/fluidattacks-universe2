# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
import re
from typing import (
    Iterator,
    List,
    Pattern,
    Tuple,
)

GEMFILE_DEP: Pattern[str] = re.compile(
    r'\s*gem\s*"(.*)",\s*?"=?\s?([\d+\.?]+)'
)
NOT_PROD_DEP: Pattern[str] = re.compile(
    r":group => \[?[:\w\-, ]*(:development|:test)"
)
NOT_PROD_GROUP: Pattern[str] = re.compile(r"(\s*)group :(test|development)")
GEM_LOCK_DEP: Pattern[str] = re.compile(r"\s+(\S+)\s+\(=?\s?([^><~,]+)\)")


@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE)
def gem_gemfile(gem_info: Tuple[str, str]) -> Iterator[DependencyType]:
    line_group: bool = False
    end_line: str = ""
    for line_number, line in enumerate(gem_info[0].splitlines(), 1):
        if line_group:
            if line == end_line:
                line_group = False
                end_line = ""
        elif match_group := re.search(NOT_PROD_GROUP, line):
            line_group = True
            blank = match_group.group(1)
            end_line = f"{blank}end"
        elif matched := re.search(GEMFILE_DEP, line):
            if re.search(NOT_PROD_DEP, line):
                continue
            pkg_name = matched.group(1)
            version = matched.group(2)
            yield format_pkg_dep(pkg_name, version, line_number)


@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE_LOCK)
def gem_gemfile_lock(gem_info: Tuple[str, str]) -> Iterator[DependencyType]:
    line_gem: bool = False
    match_arr: List[str] = []
    for line_number, line in enumerate(gem_info[0].splitlines(), 1):
        if line.startswith("GEM"):
            line_gem = True
        elif not line_gem:
            continue
        elif matched := re.match(GEM_LOCK_DEP, line):
            pkg_name = matched.group(1)
            if pkg_name in match_arr:
                continue
            match_arr.append(pkg_name)
            version = matched.group(2)
            yield format_pkg_dep(pkg_name, version, line_number)
        elif not line or not line.startswith(" "):
            break
