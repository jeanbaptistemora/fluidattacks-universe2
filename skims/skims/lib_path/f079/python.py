from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
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
    Tuple,
)
from utils.fs import (
    get_file_content_block,
)
from virtualenv import (
    cli_run,
)


def create_venv_install_requirements(filename: str) -> str:
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
    return os.getcwd()


def _get_name(dependencies: requirements.Requirement) -> str:
    return dependencies.name


def pip_incomplete_dependencies_list(
    content: str, path: str
) -> Vulnerabilities:
    build_requirements_path = (
        create_venv_install_requirements(path) + "/requirements_2.txt"
    )
    get_requirements = get_file_content_block(build_requirements_path)

    def iterator() -> Iterator[Tuple[int, int]]:
        dependencies_names = list(
            map(_get_name, list(requirements.parse(get_requirements)))
        )
        client_dependencies_names = list(
            map(_get_name, requirements.parse(content))
        )
        for line_number, name in enumerate(dependencies_names, 1):
            if name not in client_dependencies_names:
                yield line_number, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=get_requirements,
        description_key="src.lib_path.f079.pip_incomplete_dependencies_list",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PIP_INCOMPLETE_DEPENDENCIES_LIST,
    )
