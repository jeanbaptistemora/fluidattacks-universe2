from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    ParseResults,
    Regex,
)
import re


def unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    def check_regex(tokens: ParseResults) -> bool:
        for token in tokens:
            if re.fullmatch(
                r"FROM\s+[\w\/]+(\s+AS\s+\S+)?", token
            ) or re.fullmatch(
                r"FROM\s+[\w\/]+:[\w\-\.]+(\s+AS\s+\S+)?", token
            ):
                return True
        return False

    grammar = Regex(r"FROM\s+\S+")
    grammar.addCondition(check_regex)

    return get_vulnerabilities_blocking(
        content=content,
        description_key="criteria.vulns.380.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.UNPINNED_DOCKER_IMAGE,
    )


def get_values_by_key(node: Node, key: str, nodes: set[Node]) -> set[Node]:
    if isinstance(node.data, dict):
        for parent, sub_tree in node.data.items():
            if parent.data == key:
                nodes.add(sub_tree)
                return nodes
            if isinstance(sub_tree, Node):
                nodes.update(get_values_by_key(sub_tree, key, nodes))
    return nodes


def check_digest(line: str) -> bool:
    env_var_re: re.Pattern = re.compile(r"\$\{.+\}")
    digest_re: re.Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    return bool(env_var_re.search(line) or digest_re.search(line))


def _docker_compose_image_has_digest(
    template: Node,
) -> Iterator[Node]:

    if isinstance(template, Node) and (
        template_images := get_values_by_key(template, "image", set())
    ):
        for image in template_images:
            if not check_digest(image.data):
                yield image


def docker_compose_image_has_digest(
    content: str,
    path: str,
    template: Node,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f380.bash_image_has_digest",
        iterator=get_cloud_iterator(
            _docker_compose_image_has_digest(template)
        ),
        path=path,
        method=MethodsEnum.DOCKER_COMPOSE_IMAGE_HAS_DIGEST,
    )
