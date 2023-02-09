from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
    Type,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    Pattern,
    Set,
    Tuple,
)


def check_array_of_nodes(node: Node, key: str) -> Set[Node]:
    match_nodes: Set[Node] = set()
    for sub_tree in node.data:
        match_nodes.update(get_values_by_key(sub_tree, key, match_nodes))
    return match_nodes


def get_values_by_key(node: Node, key: str, nodes: Set[Node]) -> Set[Node]:
    if not isinstance(node.data, dict):
        return nodes
    for parent, sub_tree in node.data.items():
        if isinstance(sub_tree, dict):
            continue
        if parent.data == key:
            nodes.add(sub_tree)
            return nodes
        if isinstance(sub_tree, Node):
            nodes.update(get_values_by_key(sub_tree, key, nodes))
        if sub_tree.data_type == Type.ARRAY:
            nodes.update(check_array_of_nodes(sub_tree, key))
    return nodes


def check_digest(line: str) -> bool:
    env_var_re: Pattern = re.compile(r"\{.+\}")
    digest_re: Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    return bool(env_var_re.search(line) or digest_re.search(line))


def _k8s_image_has_digest(
    template: Node,
) -> Iterator[Tuple[int, int]]:
    if (
        isinstance(template, Node)
        and hasattr(template, "raw")
        and hasattr(template.raw, "get")
        and template.raw.get("apiVersion")
        and (template_images := get_values_by_key(template, "image", set()))
    ):
        vulns = filter(
            lambda image: isinstance(image.data, str)
            and not check_digest(image.data),
            template_images,
        )

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
