from contextlib import (
    suppress,
)
from lib_path.common import (
    get_vulnerabilities_for_incomplete_deps,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import os
import requirements
import subprocess  # nosec
from typing import (
    Iterator,
)
from utils.fs import (
    get_file_content_block,
)
from virtualenv import (
    cli_run,
)


def create_venv_install_requirements(filename: str) -> str:
    with suppress(FileNotFoundError):
        cli_run(["venv"])
        subprocess.call(  # nosec
            ["python", "venv/bin/activate_this.py"], shell=False
        )
        os.environ["PYTHONPATH"] = ""
        with open(filename, encoding="utf-8") as dependencies:
            reqs = dependencies.readlines()

        with open(os.devnull, "wb") as devnull:
            for item in reqs:
                subprocess.call(  # nosec
                    ["venv/bin/pip", "install", f"{item}"],
                    shell=False,
                    stdout=devnull,
                    stderr=devnull,
                )

        with open("requirements_2.txt", "w", encoding="utf-8") as outfile:
            subprocess.call(  # nosec
                ["venv/bin/pip", "freeze", "--local"],
                stdout=outfile,
                shell=False,
            )

    subprocess.call(["rm", "-rf", "venv"], shell=False)  # nosec
    return os.getcwd()


def _get_name(dependencies: requirements.requirement.Requirement) -> str:
    name: str = str(dependencies.name)
    return name


def pip_incomplete_dependencies_list(
    content: str, path: str
) -> Vulnerabilities:
    build_requirements_path = (
        create_venv_install_requirements(path) + "/requirements_2.txt"
    )
    get_requirements = get_file_content_block(build_requirements_path)
    subprocess.call(  # nosec
        ["rm", "-rf", build_requirements_path], shell=False
    )

    def iterator() -> Iterator[str]:
        dependencies_names = list(
            map(_get_name, list(requirements.parse(get_requirements)))
        )
        client_dependencies_names = list(
            map(_get_name, requirements.parse(content))
        )
        # Standardize equivalent dependencies to different hyphenated names.
        # e.g. "typing-extensions" vs "typing_extensions"
        dep_standard_names = [
            dep.replace("-", "_") for dep in dependencies_names
        ]
        client_standard_names = [
            dep.replace("-", "_") for dep in client_dependencies_names
        ]

        for name, std_name in zip(dependencies_names, dep_standard_names):
            if std_name not in client_standard_names:
                yield name

    return get_vulnerabilities_for_incomplete_deps(
        content=content,
        description_key="src.lib_path.f120.pip_incomplete_dependencies_list",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PIP_INCOMPLETE_DEPENDENCIES_LIST,
    )
