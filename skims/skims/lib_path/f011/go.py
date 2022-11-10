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
    Dict,
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
GO_REP_DEP: Pattern[str] = re.compile(
    r"replace\s(.+?/[\w\-\.~]+?)(/v\d+)?(\sv(\S+))?\s=>"
    r"\s(.+?/[\w\-\.~]+?)(/v\d+)?(\sv(\S+))?$"
)
GO_DIRECTIVE: Pattern[str] = re.compile(r"(?P<directive>require|replace) \(")
GO_VERSION: Pattern[str] = re.compile(
    r"\ngo (?P<major>\d)\.(?P<minor>\d+)(\.\d+)?\n"
)


def add_require(
    matched: Match[str], req_dict: Dict[str, DependencyType], line_number: int
) -> None:
    product = matched.group("product")
    version = matched.group("version")
    req_dict[product] = format_pkg_dep(
        product, version, line_number, line_number
    )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GO, MethodsEnum.GO_MOD)
def go_mod(content: str, path: str) -> Iterator[DependencyType]:  # NOSONAR
    go_version = GO_VERSION.search(content)
    major = int(go_version.group("major"))  # type: ignore
    minor = int(go_version.group("minor"))  # type: ignore
    if major >= 2 or (major == 1 and minor >= 17):
        required: str = ""
        replace_list: List[str] = []
        req_dict: Dict[str, DependencyType] = {}
        for line_number, line in enumerate(content.splitlines(), 1):
            if matched := re.search(GO_REQ_MOD_DEP, line):
                add_require(matched, req_dict, line_number)
            elif re.search(GO_REP_DEP, line):
                replace_list.append(line)
            elif not required:
                if directive := GO_DIRECTIVE.match(line):
                    required = directive.group("directive")
            elif required == "replace":
                if line == ")":
                    required = ""
                    continue
                replace_list.append(line)
            elif matched := re.search(GO_MOD_DEP, line):
                add_require(matched, req_dict, line_number)
            else:
                required = ""
    else:
        yield ({}, {})
