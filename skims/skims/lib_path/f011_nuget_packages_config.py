from aioextensions import (
    in_process,
)
import bs4
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from model import (
    core_model,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
)


def _check(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
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


@SHIELD
async def check(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check,
        content=content,
        finding=finding,
        path=path,
        platform=core_model.Platform.NUGET,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_name: str,
    file_extension: str,
    finding: core_model.FindingEnum,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    if (file_name, file_extension) == ("packages", "config"):
        return [
            check(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]

    return []
