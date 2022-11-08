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
    Match,
    Pattern,
)

GO_MOD_DEP: Pattern[str] = re.compile(
    r"^\s+(?P<product>.+?/[\w\-\.~]+?)(/v\d+)?\sv(?P<version>\S+)"
)
GO_REQ_MOD_DEP: Pattern[str] = re.compile(
    r"require\s(?P<product>.+?/[\w\-\.~]+?)(/v\d+)?\sv(?P<version>\S+)"
)
GO_REPLACE: Pattern[str] = re.compile(
    r"^\s+(.+?/[\w\-\.~]+?)(/v\d+)?(\sv(\S+))?\s=>"
    r"\s(.+?/[\w\-\.~]+?)(/v\d+)?(\sv(\S+))?$"
)
GO_DIRECTIVE: Pattern[str] = re.compile(r"(?P<directive>require|replace) \(")


def get_dep_info(matched: Match[str], line_number: int) -> DependencyType:
    product = matched.group("product")
    version = matched.group("version")
    return format_pkg_dep(product, version, line_number, line_number)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GO, MethodsEnum.GO_MOD)
def go_mod(content: str, path: str) -> Iterator[DependencyType]:
    required: str = ""
    replace_list: List[str] = []
    for line_number, line in enumerate(content.splitlines(), 1):
        if matched := re.search(GO_REQ_MOD_DEP, line):
            yield get_dep_info(matched, line_number)
        elif not required:
            if directive := GO_DIRECTIVE.match(line):
                required = directive.group("directive")
        elif required == "replace":
            if line == ")":
                required = ""
                continue
            replace_list.append(line)
        elif matched := re.search(GO_MOD_DEP, line):
            yield get_dep_info(matched, line_number)
        else:
            required = ""
