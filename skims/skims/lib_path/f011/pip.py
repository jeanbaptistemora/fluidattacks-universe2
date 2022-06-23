from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
import requirements
from typing import (
    Iterator,
)


def pip_requirements_txt(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_number, line in enumerate(content.split("\n"), 1):
            if line:
                for parse_dependency in requirements.parse(line):
                    yield (
                        {
                            "column": 0,
                            "line": line_number,
                            "item": parse_dependency.name,
                        },
                        {
                            "column": 0,
                            "line": line_number,
                            "item": parse_dependency.specs[0][1],
                        },
                    )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(),
        path=path,
        platform=Platform.PIP,
        method=MethodsEnum.PIP_REQUIREMENTS_TXT,
    )
