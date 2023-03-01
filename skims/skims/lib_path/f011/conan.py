import ast
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
from typing import (
    Any,
    Optional,
    Tuple,
)

CONANFILE_PY_DEP: re.Pattern[str] = re.compile(r'\s+requires\s*=\s*"[^"]*"')
SELF_REQUIRES: re.Pattern[str] = re.compile(
    r'\s+self\.requires\("(?P<pkg>[^"]+)"[^\)]*\)'
)


def get_dep_info(dep_line: str) -> tuple[str, str]:
    product, version = dep_line.strip().split("@")[0].split("/")
    if "[" in version:
        version = re.sub(r"[\[\]]", "", version).split(",")[0]
    return product, version


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_TXT)
def conan_conanfile_txt(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[requires]"):
            line_deps = True
        elif line_deps:
            if not line or line.startswith("["):
                break
            pkg_name, pkg_version = get_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


def get_conanfile_class(content: str) -> Optional[ast.ClassDef]:
    conan_tree = ast.parse(content)
    for ast_object in conan_tree.body:
        if isinstance(ast_object, ast.ClassDef):
            for param in ast_object.bases:
                if hasattr(param, "id") and param.id == "ConanFile":
                    return ast_object
    return None


def get_conan_requires(conan_class: ast.ClassDef) -> Iterator[Tuple[Any, Any]]:
    for attr in conan_class.body:
        if (
            isinstance(attr, ast.Assign)
            and hasattr(attr.targets[0], "id")
            and attr.targets[0].id == "requires"
            and hasattr(attr.value, "elts")
        ):
            for dep in attr.value.elts:
                yield dep.value, dep.lineno


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_PY)
def conan_conanfile_py(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if matched := SELF_REQUIRES.search(line):
            pkg_name, pkg_version = get_dep_info(matched.group("pkg"))
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )
        elif CONANFILE_PY_DEP.search(line):
            line_deps = True
        elif line_deps:
            if not line:
                line_deps = False
            if matched := re.search(r'"(.*)"', line):
                line = matched.group(1)
                pkg_name, pkg_version = get_dep_info(line)
                yield format_pkg_dep(
                    pkg_name, pkg_version, line_number, line_number
                )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANINFO_TXT)
def conan_conaninfo_txt(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[requires]"):
            line_deps = True
        elif line_deps:
            if not line:
                break
            pkg_name, pkg_version = get_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )
