# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from typing import (
    Iterator,
    Pattern,
    Tuple,
)


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


def check_digest(line: str) -> bool:
    env_var_re: Pattern = re.compile(r"\$\{.+\}")
    digest_re: Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    return bool(env_var_re.search(line) or digest_re.search(line))


def _docker_compose_image_has_digest(
    template: Node,
) -> Iterator[Tuple[int, int]]:
    if (
        isinstance(template, Node)
        and (template_services := template.inner.get("services"))
        and isinstance(template_services, Node)
        and isinstance(template_services.data, dict)
        and (services_dict := template_services.data.items())
    ):
        for service, service_data in services_dict:
            if (
                isinstance(service_data, Node)
                and (image := service_data.raw.get("image"))
                and not check_digest(image)
            ):
                yield service


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
