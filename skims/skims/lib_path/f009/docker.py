# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f009.utils import (
    is_key_sensitive,
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
    Any,
    Iterator,
    Pattern,
    Set,
    Tuple,
)

# Constants
WS = r"\s*"
WSM = r"\s+"
DOCKERFILE_ENV: Pattern[str] = re.compile(
    rf"^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>[^$].+?){WS}$",
)


def _iterate_docker_c_envs(template: Node) -> Iterator[Node]:
    if not isinstance(template, Node):
        return
    if template.data_type != Type.OBJECT:
        return

    if template_resources := template.inner.get("services", None):
        for resource_config in template_resources.data.values():
            if (
                resource_config.data_type == Type.OBJECT
                and "environment" in resource_config.inner
            ):
                environment = resource_config.inner["environment"]
                for env_var in environment.data:
                    yield env_var


def _docker_compose_env_secrets_iterate_vulnerabilities(
    env_vars_iterator: Iterator[Node],
) -> Iterator[Tuple[int, int]]:
    secret_smells: Set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }
    for env_var in env_vars_iterator:
        env_var_str: str = env_var.raw.lower()
        key_val = env_var_str.split("=", 1)
        secret = key_val[0]
        value = key_val[1].strip("'").strip('"') if len(key_val) > 1 else None
        if (
            (
                any(smell in secret for smell in secret_smells)
                or is_key_sensitive(secret)
            )
            and value
            and not (value.startswith("${") and value.endswith("}"))
        ):
            yield env_var  # type: ignore


def docker_compose_env_secrets(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f009.docker_compose_env_secrets",
        iterator=get_cloud_iterator(
            _docker_compose_env_secrets_iterate_vulnerabilities(
                env_vars_iterator=_iterate_docker_c_envs(template),
            )
        ),
        path=path,
        method=MethodsEnum.DOCKER_COMPOSE_ENV_SECRETS,
    )


def dockerfile_env_secrets(content: str, path: str) -> Vulnerabilities:
    secret_smells: Set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }

    def iterator() -> Iterator[Tuple[int, int]]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := DOCKERFILE_ENV.match(line):
                secret: str = match.group("key").lower()
                value: str = match.group("value").strip('"').strip("'")
                is_interpolated: bool = (
                    not (value.startswith("${") and value.endswith("}"))
                    and not value.startswith("#{")
                    and not value.endswith("}#")
                )
                if (
                    value
                    and is_interpolated
                    and (
                        any(smell in secret for smell in secret_smells)
                        or is_key_sensitive(secret)
                    )
                ):
                    column: int = match.start("value")
                    yield line_no, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f009.dockerfile_env_secrets.description",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_ENV_SECRETS,
    )
