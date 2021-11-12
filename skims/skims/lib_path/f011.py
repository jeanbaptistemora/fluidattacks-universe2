from aioextensions import (
    in_process,
)
from frozendict import (  # type: ignore
    frozendict,
)
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from model import (
    core_model,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
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


def _build_gradle(
    content: str,
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
        path=path,
        platform=platform,
    )


@SHIELD
async def build_gradle(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _build_gradle,
        content=content,
        path=path,
        platform=core_model.Platform.MAVEN,
    )


def _npm_package_lock_json(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies(obj: frozendict) -> Iterator[DependencyType]:
        for key in obj:
            if key["item"] in ("dependencies", "devDependencies"):
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "version":
                            yield product, spec_val
                            yield from resolve_dependencies(spec)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(
            obj=json_loads_blocking(content, default={}),
        ),
        path=path,
        platform=platform,
    )


@SHIELD
async def npm_package_lock_json(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _npm_package_lock_json,
        content=content,
        path=path,
        platform=core_model.Platform.NPM,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if (file_name, file_extension) == ("build", "gradle"):
        coroutines.append(
            build_gradle(
                content=await content_generator(),
                path=path,
            )
        )
    elif (file_name, file_extension) == ("package-lock", "json"):
        coroutines.append(
            npm_package_lock_json(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
