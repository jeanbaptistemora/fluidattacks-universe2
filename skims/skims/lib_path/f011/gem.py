# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
import re
from typing import (
    Callable,
    Iterator,
    List,
    Match,
    Pattern,
)


def format_dep(
    matched: Match[str], line_number: int, pkg_name: str = ""
) -> DependencyType:
    pkg_name = pkg_name or matched.group(1)
    version: str = matched.group(2)
    return (
        {
            "column": 0,
            "line": line_number,
            "item": pkg_name,
        },
        {
            "column": 0,
            "line": line_number,
            "item": version,
        },
    )


def pck_manager_file(
    content: str,
    path: str,
    platform: Platform,
    method: MethodsEnum,
    resolve_dependencies: Callable[[str], Iterator[DependencyType]],
) -> Vulnerabilities:

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(content),
        path=path,
        platform=platform,
        method=method,
    )


def gem_gemfile(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
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
        for line_number, line in enumerate(content.splitlines(), 1):
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
                yield format_dep(matched, line_number)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=Platform.GEM,
        method=MethodsEnum.GEM_GEMFILE,
    )


def gem_gemfile_lock(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        line_gem: bool = False
        form_dep: Pattern[str] = re.compile(r"\s+(\S+)\s+\(=?\s?([^><~,]+)\)")
        match_arr: List[str] = []
        for line_number, line in enumerate(content.splitlines(), 1):
            if line.startswith("GEM"):
                line_gem = True
            elif not line_gem:
                continue
            elif matched := re.match(form_dep, line):
                pkg_name = matched.group(1)
                if pkg_name in match_arr:
                    continue
                match_arr.append(pkg_name)
                yield format_dep(matched, line_number, pkg_name)
            elif not line or not line.startswith(" "):
                break

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=Platform.GEM,
        method=MethodsEnum.GEM_GEMFILE_LOCK,
    )
