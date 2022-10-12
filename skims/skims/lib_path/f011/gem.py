# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from gemfileparser import (
    GemfileParser,
)
from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
from parse_gemfile import (
    parse_line,
)
import re
from typing import (
    Iterator,
    List,
    Pattern,
)

GEMFILE_DEP: Pattern[str] = re.compile(
    r'^\s*(?P<gem>gem ".*?",?( "[><~=]{0,2}\s?[\d\.]+",?){0,2})'
)
NOT_PROD_DEP: Pattern[str] = re.compile(
    r":group => \[?[:\w\-, ]*(:development|:test)"
)
NOT_PROD_GROUP: Pattern[str] = re.compile(r"(\s*)group :(test|development)")
GEM_LOCK_DEP: Pattern[str] = re.compile(r"\s+(\S+)\s+\(=?\s?([^><~,]+)\)")


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE)
def gem_gemfile(  # NOSONAR
    content: str, path: str
) -> Iterator[DependencyType]:
    line_group: bool = False
    end_line: str = ""
    for line_number, line in enumerate(content.splitlines(), 1):
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
            line = GemfileParser.preprocess(matched.group("gem"))
            line = line[3:]
            product, version = parse_line(line)
            yield format_pkg_dep(product, version, line_number, line_number)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE_LOCK)
def gem_gemfile_lock(content: str, path: str) -> Iterator[DependencyType]:
    line_gem: bool = False
    match_arr: List[str] = []
    for line_number, line in enumerate(content.splitlines(), 1):
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
            yield format_pkg_dep(pkg_name, version, line_number, line_number)
        elif not line or not line.startswith(" "):
            break
