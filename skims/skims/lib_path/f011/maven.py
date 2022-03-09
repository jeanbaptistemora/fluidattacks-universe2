import bs4
from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
import re
from typing import (
    Dict,
    Iterator,
    Pattern,
    Tuple,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_LINE_COMMENT: Pattern[str] = re.compile(r"^.*" fr"{WS}//" r".*$")
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


def avoid_cmt(line: str, is_block_cmt: bool) -> Tuple[str, bool]:
    if RE_LINE_COMMENT.match(line):
        line = line.split("//", 1)[0]
    if is_block_cmt:
        if "*/" in line:
            is_block_cmt = False
            line = line.split("*/", 1).pop()
        else:
            return "", is_block_cmt
    if "/*" in line:
        line_cmt_open = line.split("/*", 1)[0]
        if "*/" in line:
            line = line_cmt_open + line.split("*/", 1).pop()
        else:
            line = line_cmt_open
            is_block_cmt = True
    return line, is_block_cmt


def resolve_dependencies_helper(content: str) -> Iterator[DependencyType]:
    is_block_cmt = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        line, is_block_cmt = avoid_cmt(line, is_block_cmt)
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


def maven_gradle(content: str, path: str) -> Vulnerabilities:

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies_helper(content),
        path=path,
        platform=Platform.MAVEN,
        method=MethodsEnum.MAVEN_GRADLE,
    )


def maven_pom_xml(content: str, path: str) -> Vulnerabilities:
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
        path=path,
        platform=Platform.MAVEN,
        method=MethodsEnum.MAVEN_POM_XML,
    )


def maven_sbt(content: str, path: str) -> Vulnerabilities:
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
        path=path,
        platform=Platform.MAVEN,
        method=MethodsEnum.MAVEN_SBT,
    )
