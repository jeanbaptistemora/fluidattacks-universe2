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
import re
from typing import (
    Iterator,
    Pattern,
    Tuple,
)
from utils.function import (
    get_node_by_keys,
)


def check_digest(line: str) -> bool:
    env_var_re: Pattern = re.compile(r"\$\{.+\}")
    digest_re: Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    return bool(env_var_re.search(line) or digest_re.search(line))


def _k8s_image_has_digest(
    template: Node,
) -> Iterator[Tuple[int, int]]:
    if (
        isinstance(template, Node)
        and template.raw.get("apiVersion")
        and (containers := get_node_by_keys(template, ["spec", "containers"]))
    ):
        image_nodes = [
            container.inner.get("image") for container in containers.data
        ]
        vulns = filter(lambda node: not check_digest(node.data), image_nodes)

        yield from vulns


def k8s_image_has_digest(
    content: str,
    path: str,
    template: Node,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f426.k8s_image_has_digest",
        iterator=get_cloud_iterator(_k8s_image_has_digest(template)),
        path=path,
        method=MethodsEnum.K8S_IMAGE_HAS_DIGEST,
    )
