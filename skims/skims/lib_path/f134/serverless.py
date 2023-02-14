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
from typing import (
    Any,
    Iterator,
    Tuple,
)


def aux_validate_type(template: Node) -> bool:
    if not isinstance(template, Node):
        return True
    if template.data_type != Type.OBJECT:
        return True
    return False


def aux_iterate_serverless_envs(resource_config: Node) -> bool:
    if (
        resource_config.data_type == Type.OBJECT
        and "events" in resource_config.inner
    ):
        return True
    return False


def _iterate_serverless_envs(template: Node) -> Iterator[Node]:
    if aux_validate_type(template):
        return
    if template_resources := template.inner.get("functions", None):
        for resource_config in template_resources.data.values():
            if aux_iterate_serverless_envs(resource_config):
                fn_events = resource_config.inner["events"]
                for event in fn_events.data if fn_events.data else []:
                    yield event


def _serverless_iterate_vulnerabilities(
    env_vars_iterator: Iterator[Node],
) -> Iterator[Tuple[int, int]]:
    for env_var in env_vars_iterator:
        if http := env_var.inner.get("http"):
            cors = (
                http.inner.get("cors") if hasattr(http.inner, "get") else None
            )
            if (
                cors
                and cors.data_type == Type.OBJECT
                and (origin := cors.inner.get("origin"))
                and origin
                and origin.raw == "*"
            ):
                yield origin


def severless_cors_wildcard(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f134.cfn_wildcard_in_allowed_origins",
        iterator=get_cloud_iterator(
            _serverless_iterate_vulnerabilities(
                env_vars_iterator=_iterate_serverless_envs(template),
            )
        ),
        path=path,
        method=MethodsEnum.YML_SERVERLESS_CORS,
    )
