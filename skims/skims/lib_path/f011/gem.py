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
    Pattern,
)


def gem_gemfile(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_number, line in enumerate(content.splitlines(), 1):
            if not line:
                continue
            if not line.startswith("gem "):
                continue
            line = GemfileParser.preprocess(line)
            line = line[3:]
            line_items = parse_line(line, "Gemfile")
            yield (
                {
                    "column": 0,
                    "line": line_number,
                    "item": line_items.get("name"),
                },
                {
                    "column": 0,
                    "line": line_number,
                    "item": line_items.get("requirement"),
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
        format_deps: Pattern[str] = re.compile(r"\s+(.*\([^><~,]+\))")
        for line_number, line in enumerate(content.splitlines(), 1):
            if line.startswith("GEM"):
                line_gem = True
            elif not line_gem:
                continue
            elif matched := re.match(format_deps, line):
                line = matched.group(1)
                line = GemfileParser.preprocess(line)
                line_items = parse_line(line, "Gemfile.lock")
                packg_name = line_items.get("name")
                version = line_items.get("requirement")
                yield (
                    {
                        "column": 0,
                        "line": line_number,
                        "item": packg_name,
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
