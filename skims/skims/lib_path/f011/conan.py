from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
from typing import (
    Iterator,
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_TXT)
def conan_conanfile_txt(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[requires]"):
            line_deps = True
        elif line_deps:
            if not line:
                break
            pkg_name, pkg_version = line.split("/")
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )