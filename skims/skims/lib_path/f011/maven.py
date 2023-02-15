import bs4
from collections.abc import (
    Iterator,
)
import glob
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
)
from utils.fs import (
    get_file_content_block,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_LINE_COMMENT: re.Pattern[str] = re.compile(r"^.*" rf"{WS}//" r".*$")
RE_GRADLE_A: re.Pattern[str] = re.compile(
    r"^.*"
    rf"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    rf"group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}"
    rf",{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}"
    rf"(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?"
    rf".*$"
)
RE_GRADLE_B: re.Pattern[str] = re.compile(
    r"^.*"
    rf"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    rf"{QUOTE}(?P<statement>{TEXT}){QUOTE}"
    rf".*$"
)
RE_SBT: re.Pattern[str] = re.compile(
    r"^[^%]*"
    rf"{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}%"
    rf"{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}%"
    rf"{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS}"
    r".*$"
)


def _get_properties(root: bs4.BeautifulSoup) -> dict[str, str]:
    return {
        property.name.lower(): property.get_text()
        for properties in root.find_all("properties", limit=2)
        for property in properties.children
        if isinstance(property, bs4.element.Tag)
    }


def avoid_cmt(line: str, is_block_cmt: bool) -> tuple[str, bool]:
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


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_GRADLE)
def maven_gradle(content: str, path: str) -> Iterator[DependencyType]:
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
        # https://gitlab.com/fluidattacks/universe/-/issues/5635
        if version == "":
            continue

        yield format_pkg_dep(product, version, line_no, line_no, column)


def _is_pom_xml(content: str) -> bool:
    root = bs4.BeautifulSoup(content, features="html.parser")
    if root.project and root.project.get("xmlns"):
        is_pom_xml = (
            str(root.project["xmlns"]) == "http://maven.apache.org/POM/4.0.0"
        )
        return is_pom_xml
    return False


def _get_parent_paths(path: str) -> list[str]:
    paths: list[str] = []
    split_path: list[str] = path.split("/")
    for pos in range(1, len(split_path) - 1):
        paths.append("/".join(split_path[0:pos]))
    return paths[::-1]


def _interpolate(path: str, value: str) -> list[Any]:
    is_match: bool = False
    content = get_file_content_block(path)

    if _is_pom_xml(content):
        root = bs4.BeautifulSoup(content, features="html.parser")
        properties = _get_properties(root)
        for var, var_value in properties.items():
            if re.search(rf"\$\{{{var}\}}", value):
                is_match = True
                value = value.replace(f"${{{var}}}", var_value)

    return [is_match, value]


def _find_vars(value: str, path: str) -> str:
    dir_paths = _get_parent_paths(path)
    is_match, interpolated_value = _interpolate(path, value)
    if is_match:
        return interpolated_value

    for dir_path in dir_paths:
        pom_files = glob.glob(f"{dir_path}/*.xml", recursive=False)
        for pom_file in pom_files:
            flag, interpolated_value = _interpolate(pom_file, value)
            if flag:
                return interpolated_value
    return interpolated_value


@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_POM_XML)
def maven_pom_xml(content: str, path: str) -> Iterator[DependencyType]:
    root = bs4.BeautifulSoup(content, features="html.parser")

    for group, artifact, version in [
        (group, artifact, version)
        for dependency in root.find_all("dependency", recursive=True)
        for group in dependency.find_all("groupid", limit=1)
        for artifact in dependency.find_all("artifactid", limit=1)
        for version in (dependency.find_all("version", limit=1) or [None])
    ]:
        g_text = _find_vars(group.get_text(), path)
        a_text = _find_vars(artifact.get_text(), path)
        if version is None:
            continue
        product = f"{g_text}:{a_text}"
        v_text = _find_vars(version.get_text(), path)
        column = version.sourcepos
        line = version.sourceline

        yield format_pkg_dep(product, v_text, line, line, column)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_SBT)
def maven_sbt(content: str, path: str) -> Iterator[DependencyType]:
    for line_no, line in enumerate(content.splitlines(), start=1):
        if match := RE_SBT.match(line):
            column: int = match.start("group")
            product: str = match.group("group") + ":" + match.group("name")
            version = match.group("version")
        else:
            continue

        yield format_pkg_dep(product, version, line_no, line_no, column)
