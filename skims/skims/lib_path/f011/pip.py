from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
import os
import requirements
import subprocess  # nosec
from typing import (
    Iterator,
)
from virtualenv import (
    cli_run,
)


def create_venv_install_requirements(filename: str) -> None:
    cli_run(["venv"])
    subprocess.call(  # nosec
        ["python", "venv/bin/activate_this.py"], shell=False
    )
    os.environ["PYTHONPATH"] = ""
    with open(filename, encoding="utf-8") as dependencies:
        reqs = dependencies.readlines()

    for item in reqs:
        subprocess.call(  # nosec
            ["venv/bin/pip", "install", f"{item}"], shell=False
        )

    with open("requirements_2.txt", "w", encoding="utf-8") as outfile:
        subprocess.call(  # nosec
            ["venv/bin/pip", "freeze", "--local"], stdout=outfile, shell=False
        )

    subprocess.call(["rm", "-rf", "venv"], shell=False)  # nosec


def pip_requirements_txt(content: str, path: str) -> Vulnerabilities:
    def resolve_dependencies() -> Iterator[DependencyType]:
        for line_number, line in enumerate(content.splitlines(), 1):
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
