from aioextensions import (
    in_process,
)
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from model import (
    core_model,
)
import re
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Pattern,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_MAVEN_A: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|implementation){WS}[(]?{WS}"
    fr"group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}"
    fr",{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}"
    fr"(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?"
    fr".*$"
)
RE_MAVEN_B: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|implementation){WS}[(]?{WS}"
    fr"{QUOTE}(?P<statement>{TEXT}){QUOTE}"
    fr".*$"
)


def _check(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := RE_MAVEN_A.match(line):
                column: int = match.start("group")
                product: str = match.group("group") + ":" + match.group("name")
                version: str = match.group("version") or "*"
            elif match := RE_MAVEN_B.match(line):
                column = match.start("statement")
                statement = match.group("statement")
                product, version = (
                    statement.rsplit(":", maxsplit=1)
                    if statement.count(":") >= 2
                    else (statement, "*")
                )
            else:
                continue

            yield (
                {"column": column, "line": line_no, "item": product},
                {"column": column, "line": line_no, "item": version},
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
        platform=core_model.Platform.MAVEN,
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
    if (file_name, file_extension) == ("build", "gradle"):
        return [
            check(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]

    return []
