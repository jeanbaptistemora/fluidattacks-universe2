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


def format_conan_dep_info(dep_info: ast.Constant) -> DependencyType:
    pkg_name, pkg_version = get_dep_info(dep_info.value)
    line_num = dep_info.lineno
    col_num = dep_info.col_offset + 1
    return format_pkg_dep(pkg_name, pkg_version, line_num, line_num, col_num)


def get_conanfile_class(content: str) -> ast.ClassDef | None:
    conan_tree = ast.parse(content)
    for ast_object in conan_tree.body:
        if isinstance(ast_object, ast.ClassDef):
            for param in ast_object.bases:
                if hasattr(param, "id") and param.id == "ConanFile":
                    return ast_object
    return None


def get_conan_requires(conan_class: ast.ClassDef) -> Iterator[DependencyType]:
    for attr in conan_class.body:
        if (
            isinstance(attr, ast.Assign)
            and hasattr(attr.targets[0], "id")
            and attr.targets[0].id == "requires"
            and hasattr(attr.value, "elts")
        ):
            yield from (
                format_conan_dep_info(dep_info) for dep_info in attr.value.elts
            )


def get_conan_self_requires(
    conan_class: ast.ClassDef,
) -> Iterator[DependencyType]:
    for node in conan_class.body:
        if isinstance(node, ast.FunctionDef) and node.name == "requirements":
            for child_node in ast.walk(node):
                if (
                    isinstance(child_node, ast.Expr)
                    and hasattr(child_node.value, "func")
                    and hasattr(child_node.value, "args")
                    and child_node.value.func.value.id == "self"
                    and child_node.value.func.attr == "requires"
                ):
                    yield format_conan_dep_info(child_node.value.args[0])


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_PY)
def conan_conanfile_py(content: str, path: str) -> Iterator[DependencyType]:
    conan_class = get_conanfile_class(content)
    if conan_class:
        yield from get_conan_requires(conan_class)
    for line_number, line in enumerate(content.splitlines(), 1):
        if matched := SELF_REQUIRES.search(line):
            pkg_name, pkg_version = get_dep_info(matched.group("pkg"))
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
