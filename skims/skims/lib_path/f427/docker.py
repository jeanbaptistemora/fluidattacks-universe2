from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_vulnerabilities_include_parameter,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re


def docker_port_exposed(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int, str]]:
        unsafe_ports = r"(20|21|23|25|53|69|80|137|139|445|8080)$"
        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.startswith("EXPOSE"):
                for port in line.split(" ")[1:]:
                    if (port := re.split("/", port)[0]) and (
                        re.match(unsafe_ports, port)
                    ):
                        yield (line_number, 0, port)

    return get_vulnerabilities_include_parameter(
        content=content,
        description_key="lib_path.f427.docker_port_exposed",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_PORT_EXPOSED,
    )
