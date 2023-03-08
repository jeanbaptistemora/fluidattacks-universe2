import ast
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    DependencyType,
    format_conan_dep_info,
    format_pkg_dep,
    get_conan_dep_info,
    get_conanfile_class,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)


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
            pkg_name, pkg_version = get_conan_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


def get_conan_requires(attr: ast.Assign) -> Iterator[DependencyType]:
    if hasattr(attr.targets[0], "id") and attr.targets[0].id == "requires":
        requires = attr.value
        if isinstance(requires, ast.Constant):
            yield format_conan_dep_info(requires)
        elif hasattr(requires, "elts"):
            for dep_info in requires.elts:
                if isinstance(dep_info, ast.Constant):
                    yield format_conan_dep_info(dep_info)
                elif hasattr(dep_info, "elts"):
                    yield format_conan_dep_info(dep_info.elts[0])


def get_conan_self_requires(
    node: ast.FunctionDef,
) -> Iterator[DependencyType]:
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
        for node in conan_class.body:
            if isinstance(node, ast.Assign):
                yield from get_conan_requires(node)
            elif (
                isinstance(node, ast.FunctionDef)
                and node.name == "requirements"
            ):
                yield from get_conan_self_requires(node)


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
            pkg_name, pkg_version = get_conan_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )
