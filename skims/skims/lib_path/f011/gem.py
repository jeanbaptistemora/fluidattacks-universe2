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
    Iterator,
    List,
    Pattern,
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
                pkg_name: str = matched.group(1)
                version: str = matched.group(2)
                yield (
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
                pck_name = matched.group(1)
                version = matched.group(2)
                if pck_name in match_arr:
                    continue
                match_arr.append(pck_name)
                yield (
                    {
                        "column": 0,
                        "line": line_number,
                        "item": pck_name,
                    },
                    {
                        "column": 0,
                        "line": line_number,
                        "item": version,
                    },
                )
            elif not line or not line.startswith(" "):
                break

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=Platform.GEM,
        method=MethodsEnum.GEM_GEMFILE_LOCK,
    )
