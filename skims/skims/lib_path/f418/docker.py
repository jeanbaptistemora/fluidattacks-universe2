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


def _docker_compose_read_only(template: Node) -> Iterator[Tuple[int, int]]:
    if (
        isinstance(template, Node)
        and (template_services := template.inner.get("services"))
        and isinstance(template_services, Node)
    ):
        if isinstance(template_services.data, dict) and (
            services_dict := template_services.data.items()
        ):
            for service, service_data in services_dict:
                if (
                    isinstance(service_data, Node)
                    and service_data.raw.get("read_only") is not True
                ):
                    yield service


def docker_compose_read_only(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f418.docker_compose_read_only",
        iterator=get_cloud_iterator(_docker_compose_read_only(template)),
        path=path,
        method=MethodsEnum.DOCKER_COMPOSE_READ_ONLY,
    )


def docker_port_22_exposed(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.match(r"^EXPOSE[ \t]+22", line):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f418.docker_port_22_exposed",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_PORT_22_EXPOSED,
    )


def docker_using_add_command(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.match(r"^ADD[ \t]+\w", line):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f418.docker_using_add_command",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_USING_ADD_COMMAND,
    )
