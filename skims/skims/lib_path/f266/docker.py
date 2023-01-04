from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Any,
    Iterator,
    Tuple,
)

COMMANDS_REGEX = [
    re.compile(r"(\s+|^RUN).*useradd"),
    re.compile(r"(\s+|^RUN).*adduser"),
    re.compile(r"(\s+|^RUN).*addgroup"),
    re.compile(r"(\s+|^RUN).*usergroup"),
    re.compile(r"(\s+|^RUN).*usermod"),
    re.compile(r"^USER"),
]


def get_container_image(content: str) -> bool:
    for _, line in enumerate(content.splitlines(), start=1):
        if re.match(r"FROM\s+\S+", line):
            return True
    return False


def container_without_user(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        no_line = (0, 0)
        has_user = False
        for _, line in enumerate(content.splitlines(), start=1):
            if any(regex.match(line) for regex in COMMANDS_REGEX):
                has_user = True
        if get_container_image(content) and not has_user:
            yield no_line

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.container_without_user",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WITHOUT_USER,
    )


def container_with_user_root(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.match(r"^USER root", line):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.docker_with_user_root",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WITH_USER_ROOT,
    )


def _docker_compose_without_user(template: Node) -> Iterator[Tuple[int, int]]:
    if (  # pylint: disable=too-many-boolean-expressions
        isinstance(template, Node)
        and (hasattr(template.inner, "get"))
        and (template_services := template.inner.get("services"))
        and isinstance(template_services, Node)
        and isinstance(template_services.data, dict)
        and (services_dict := template_services.data.items())
    ):
        for service, service_data in services_dict:
            if (
                isinstance(service_data, Node)
                and service_data.raw.get("user") is None
            ):
                yield service


def docker_compose_without_user(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.docker_compose_without_user",
        iterator=get_cloud_iterator(_docker_compose_without_user(template)),
        path=path,
        method=MethodsEnum.DOCKER_COMPOSE_WITHOUT_USER,
    )
