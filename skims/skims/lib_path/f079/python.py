from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import os
import subprocess  # nosec
from typing import (
    Iterator,
    Tuple,
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


def pip_incomplete_dependencies_list(
    content: str, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        yield 0, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f009.dockerfile_env_secrets.description",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_ENV_SECRETS,
    )
