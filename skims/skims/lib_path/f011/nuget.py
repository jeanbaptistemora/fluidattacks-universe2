import bs4
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


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.NUGET, MethodsEnum.NUGET_CSPROJ)
def nuget_csproj(content: str, path: str) -> Iterator[DependencyType]:
    root = bs4.BeautifulSoup(content, features="html.parser")

    for pkg in root.find_all("packagereference", recursive=True):
        if (id_ := pkg.get("include")) and (version := pkg.get("version")):
            column = pkg.sourcepos
            line = pkg.sourceline

            yield format_pkg_dep(id_, version, line, line, column)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.NUGET, MethodsEnum.NUGET_PACKAGES_CONFIG)
def nuget_pkgs_config(content: str, path: str) -> Iterator[DependencyType]:
    root = bs4.BeautifulSoup(content, features="html.parser")

    for pkg in root.find_all("package", recursive=True):
        if (id_ := pkg.get("id")) and (version := pkg.get("version")):
            column = pkg.sourcepos
            line = pkg.sourceline

            yield format_pkg_dep(id_, version, line, line, column)
