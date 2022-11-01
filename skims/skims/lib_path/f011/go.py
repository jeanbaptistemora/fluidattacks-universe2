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
    Pattern,
)

GO_MOD_DEP: Pattern[str] = re.compile(
    r"\s+(?P<product>.+?/[\w\-\.~]+?)(/v\d+)?\sv(?P<version>\S+)"
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GO, MethodsEnum.GO_MOD)
def go_mod(content: str, path: str) -> Iterator[DependencyType]:
    required: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if not required:
            if line.startswith("require"):
                required = True
        elif matched := re.search(GO_MOD_DEP, line):
            product = matched.group("product")
            version = matched.group("version")
            yield format_pkg_dep(product, version, line_number, line_number)
        else:
            required = False
