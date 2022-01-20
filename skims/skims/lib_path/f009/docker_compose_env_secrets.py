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
    FindingEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
    Set,
    Tuple,
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
            yield env_var


def docker_compose_env_secrets(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.docker_compose_env_secrets",
        finding=FindingEnum.F009,
        iterator=get_cloud_iterator(
            _docker_compose_env_secrets_iterate_vulnerabilities(
                env_vars_iterator=_iterate_docker_c_envs(template),
            )
        ),
        path=path,
    )
