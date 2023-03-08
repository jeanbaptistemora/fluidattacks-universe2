from collections.abc import (
    Iterator,
)
from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    get_conan_dep_info,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
import re

SELF_TOOL_DEPS: re.Pattern[str] = re.compile(
    r'\s+self\.(tool|build)_requires\("(?P<pkg>[^"]+)"[^\)]*\)'
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_TXT_DEV)
def conan_conanfile_txt_dev(
    content: str, path: str
) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if re.search(r"^\[(tool|build)_requires\]$", line):
            line_deps = True
        elif line_deps:
            if not line or line.startswith("["):
                break
            pkg_name, pkg_version = get_conan_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_PY_DEV)
def conan_conanfile_py_dev(
    content: str, path: str
) -> Iterator[DependencyType]:
    for line_number, line in enumerate(content.splitlines(), 1):
        if matched := SELF_TOOL_DEPS.search(line):
            pkg_name, pkg_version = get_conan_dep_info(matched.group("pkg"))
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANINFO_TXT_DEV)
def conan_conaninfo_txt_dev(
    content: str, path: str
) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[build_requires]"):
            line_deps = True
        elif line_deps:
            if not line:
                break
            pkg_name, pkg_version = get_conan_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )
