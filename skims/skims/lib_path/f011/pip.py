# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
import requirements
from typing import (
    Iterator,
)


def pip_requirements_txt(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_number, line in enumerate(content.splitlines(), 1):
            if line:
                for parse_dependency in requirements.parse(line):
                    product = parse_dependency.name
                    version = parse_dependency.specs[0][1]

                    yield format_pkg_dep(
                        product, version, line_number, line_number
                    )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=Platform.PIP,
        method=MethodsEnum.PIP_REQUIREMENTS_TXT,
    )
