from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    FindingEnum,
    Platform,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    Pattern,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_SBT: Pattern[str] = re.compile(
    r"^[^%]*"
    fr"{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}%"
    fr"{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}%"
    fr"{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS}"
    r".*$"
)


def maven_sbt(
    content: str, finding: FindingEnum, path: str, platform: Platform
) -> Vulnerabilities:
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
