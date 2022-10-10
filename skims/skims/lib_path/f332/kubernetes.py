# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from typing import (
    Any,
    Dict,
    Iterator,
    Tuple,
)
from utils.function import (
    get_node_by_keys,
)


def check_port(port: Node) -> bool:
    port_80 = False
    protocol_tcp = False
    if isinstance(port.data, Dict):
        for key, val in port.data.items():
            if (
                isinstance(key, Node)
                and isinstance(val, Node)
                and (key.data == "port")
                and (val.data == 80)
            ):
                port_80 = True
            if (
                isinstance(key, Node)
                and isinstance(val, Node)
                and (key.data == "protocol")
                and (val.data == "TCP")
            ):
                protocol_tcp = True
        if port_80 and protocol_tcp:
            return True
    return False


def _kubernetes_insecure_port(template: Node) -> Iterator[Tuple[int, int]]:
    if (
        isinstance(template, Node)
        and template.raw.get("apiVersion")
        and (ports := get_node_by_keys(template, ["spec", "ports"]))
    ):
        yield from iter(port for port in ports.data if check_port(port))


def kubernetes_insecure_port(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f332.kubernetes_insecure_port",
        iterator=get_cloud_iterator(_kubernetes_insecure_port(template)),
        path=path,
        method=MethodsEnum.KUBERNETES_INSECURE_PORT,
    )
