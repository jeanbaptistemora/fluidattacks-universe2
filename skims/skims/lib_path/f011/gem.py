# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from gemfileparser import (
    GemfileParser,
)
from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
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


def gem_gemfile(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        form_req: Pattern[str] = re.compile(
            r"^gem\s*.*,[^><~!]*(=?\s?[\d+\.?]+)"
        )
        equal_patt: Pattern[str] = re.compile(r"= ?")
        not_prod_patt: Pattern[str] = re.compile(
            r":group => \[?[:\w\-, ]*(:development|:test)"
        )
        for line_number, line in enumerate(content.splitlines(), 1):
            if not line:
                continue
            if not re.search(form_req, line):
                continue
            if re.search(not_prod_patt, line):
                continue
            line = GemfileParser.preprocess(line)
            line = line[3:]
            line_items = parse_line(line)
            line_version: str = line_items["requirement"]
            version = re.sub(equal_patt, "", line_version)
            yield (
                {
                    "column": 0,
                    "line": line_number,
                    "item": line_items.get("name"),
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
