from metaloaders.model import (
    Node,
)
from typing import (
    Iterator,
)


def is_privileged(sec_ctx: Node) -> bool:
    privileged = sec_ctx.inner.get("privileged")
    if privileged and privileged.data:
        return True
    return False


def iter_containers_type(
    template: Node,
) -> Iterator[Node]:
    containers_type = {
        "containers",
        "ephemeralContainers",
        "containers",
    }
    if template and template.data:
        k8s_spec = template.inner.get("spec", None)
        if k8s_spec and k8s_spec.data:
            for c_type in containers_type:
                if container := k8s_spec.inner.get(c_type, None):
                    yield container.data


def get_containers_capabilities(sec_ctx: Node, type_cap: str) -> list:
    cap = sec_ctx.inner.get("capabilities", None)
    if cap and cap.data:
        add = cap.inner.get(type_cap, None)
        if add and add.data:
            return add.data
    return []


def iter_security_context(template: Node, upper_level: bool) -> Iterator[Node]:
    if template.raw.get("apiVersion"):
        if upper_level:
            ctx = template.inner.get("securityContext", None)
            if ctx and ctx.data:
                yield ctx
        for container in iter_containers_type(template):
            for elem in container:
                ctx = elem.inner.get("securityContext", None)
                if ctx and ctx.data:
                    yield ctx
