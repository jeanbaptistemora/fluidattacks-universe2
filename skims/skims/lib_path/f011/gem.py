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


@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE)
def gem_gemfile(gem_info: Tuple[str, str]) -> Iterator[DependencyType]:
    require_patt: Pattern[str] = re.compile(
        r'\s*gem\s*"(.*)",\s*?"=?\s?([\d+\.?]+)'
    )
    not_prod_patt: Pattern[str] = re.compile(
        r":group => \[?[:\w\-, ]*(:development|:test)"
    )
    test_dev_group_patt: Pattern[str] = re.compile(
        r"(\s*)group :(test|development)"
    )
    line_group: bool = False
    end_line: str = ""
    for line_number, line in enumerate(gem_info[0].splitlines(), 1):
        if line_group:
            if line == end_line:
                line_group = False
                end_line = ""
        elif match_group := re.search(test_dev_group_patt, line):
            line_group = True
            blank = match_group.group(1)
            end_line = f"{blank}end"
        elif matched := re.search(require_patt, line):
            if re.search(not_prod_patt, line):
                continue
            pkg_name = matched.group(1)
            version = matched.group(2)
            yield format_pkg_dep(pkg_name, version, line_number)


@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE_LOCK)
def gem_gemfile_lock(gem_info: Tuple[str, str]) -> Iterator[DependencyType]:
    line_gem: bool = False
    form_dep: Pattern[str] = re.compile(r"\s+(\S+)\s+\(=?\s?([^><~,]+)\)")
    match_arr: List[str] = []
    for line_number, line in enumerate(gem_info[0].splitlines(), 1):
        if line.startswith("GEM"):
            line_gem = True
        elif not line_gem:
            continue
        elif matched := re.match(form_dep, line):
            pkg_name = matched.group(1)
            if pkg_name in match_arr:
                continue
            match_arr.append(pkg_name)
            version = matched.group(2)
            yield format_pkg_dep(pkg_name, version, line_number)
        elif not line or not line.startswith(" "):
            break
