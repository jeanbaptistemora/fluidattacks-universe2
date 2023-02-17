from collections.abc import (
    Iterator,
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
import re


def get_dep_info(dep_line: str) -> tuple[str, str]:
    product, version = dep_line.lstrip().split("@")[0].split("/")
    if "[" in version:
        version = re.sub(r"[\[\]]", "", version).split(",")[0]
    return product, version


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_TXT_DEV)
def conan_conanfile_txt_dev(
    content: str, path: str
) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[tool_requires]"):
            line_deps = True
        elif line_deps:
            if not line:
                break
            pkg_name, pkg_version = get_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_PY_DEV)
def conan_conanfile_py_dev(
    content: str, path: str
) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("build_requires"):
            line_deps = True
        elif line_deps:
            if not line:
                break
            pkg_name, pkg_version = get_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )
