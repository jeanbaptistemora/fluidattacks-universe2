import bs4
from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    FindingEnum,
    Platform,
    Vulnerabilities,
)
from typing import (
    Iterator,
)


def nuget_packages_config(
    content: str, finding: FindingEnum, path: str, platform: Platform
) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        root = bs4.BeautifulSoup(content, features="html.parser")

        for pkg in root.find_all("package", recursive=True):
            if (id_ := pkg.get("id")) and (version := pkg.get("version")):
                column = pkg.sourcepos
                line = pkg.sourceline

                yield (
                    {"column": column, "line": line, "item": id_},
                    {"column": column, "line": line, "item": version},
                )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        finding=finding,
        path=path,
        platform=platform,
    )
