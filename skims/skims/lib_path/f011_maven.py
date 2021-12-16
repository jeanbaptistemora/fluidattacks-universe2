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
import re
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Pattern,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_GRADLE_A: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    fr"group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}"
    fr",{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}"
    fr"(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?"
    fr".*$"
)
RE_GRADLE_B: Pattern[str] = re.compile(
    r"^.*"
    fr"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    fr"{QUOTE}(?P<statement>{TEXT}){QUOTE}"
    fr".*$"
)
RE_SBT: Pattern[str] = re.compile(
    r"^[^%]*"
    fr"{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}%"
    fr"{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}%"
    fr"{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS}"
    r".*$"
)


def _get_properties(root: bs4.BeautifulSoup) -> Dict[str, str]:
    return {
        property.name.lower(): property.get_text()
        for properties in root.find_all("properties", limit=2)
        for property in properties.children
        if isinstance(property, bs4.element.Tag)
    }


def _interpolate(properties: Dict[str, str], value: str) -> str:
    for var, var_value in properties.items():
        value = value.replace(f"${{{var}}}", var_value)

    return value


def _check_maven_pom_xml(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        root = bs4.BeautifulSoup(content, features="html.parser")

        properties = _get_properties(root)

        for group, artifact, version in [
            (group, artifact, version)
            for dependency in root.find_all("dependency", recursive=True)
            for group in dependency.find_all("groupid", limit=1)
            for artifact in dependency.find_all("artifactid", limit=1)
            for version in (dependency.find_all("version", limit=1) or [None])
        ]:
            g_text = _interpolate(properties, group.get_text())
            a_text = _interpolate(properties, artifact.get_text())
            if version is None:
                v_text = _interpolate(properties, "*")
                column = artifact.sourcepos
                line = artifact.sourceline
            else:
                v_text = _interpolate(properties, version.get_text())
                column = version.sourcepos
                line = version.sourceline

            yield (
                {"column": column, "line": line, "item": f"{g_text}:{a_text}"},
                {"column": column, "line": line, "item": v_text},
            )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        finding=finding,
        path=path,
        platform=platform,
    )


@SHIELD
async def check_maven_pom_xml(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check_maven_pom_xml,
        content=content,
        finding=finding,
        path=path,
        platform=core_model.Platform.MAVEN,
    )


def _check_maven_gradle(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := RE_GRADLE_A.match(line):
                column: int = match.start("group")
                product: str = match.group("group") + ":" + match.group("name")
                version = match.group("version") or ""
            elif match := RE_GRADLE_B.match(line):
                column = match.start("statement")
                statement = match.group("statement")
                product, version = (
                    statement.rsplit(":", maxsplit=1)
                    if statement.count(":") >= 2
                    else (statement, "")
                )
            else:
                continue

            # Assuming a wildcard in Maven if the version is not found can
            # result in issues.
            # https://gitlab.com/fluidattacks/product/-/issues/5635
            if version == "":
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
async def check_maven_gradle(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check_maven_gradle,
        content=content,
        finding=finding,
        path=path,
        platform=core_model.Platform.MAVEN,
    )


def _check_maven_sbt(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := RE_SBT.match(line):
                column: int = match.start("group")
                product: str = match.group("group") + ":" + match.group("name")
                version = match.group("version")
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
async def check_maven_sbt(
    content: str,
    finding: core_model.FindingEnum,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check_maven_sbt,
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
    if (file_name, file_extension) == ("pom", "xml"):
        return [
            check_maven_pom_xml(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]
    if file_extension == "gradle":
        return [
            check_maven_gradle(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]
    if (file_name, file_extension) == ("build", "sbt"):
        return [
            check_maven_sbt(
                content=await content_generator(),
                finding=finding,
                path=path,
            )
        ]

    return []
