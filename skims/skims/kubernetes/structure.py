from metaloaders.model import (
    Node,
)
from typing import (
    Iterator,
)


def is_kubernetes(template: Node) -> bool:
    cond = template and template.data and isinstance(template.inner, dict)
    if cond and (
        list(template.inner.keys())
        and list(template.inner.keys())[0] == "apiVersion"
    ):
        return True
    return False


def is_privileged(container: Node) -> bool:
    if container and container.data:
        sec_ctx = container.inner.get("securityContext")
        if sec_ctx:
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


def get_containers_capabilities(container: Node, type_cap: str) -> list:
    if container and container.data:
        sec_cont = container.inner.get("securityContext", None)
    if sec_cont and sec_cont.data:
        cap = sec_cont.inner.get("capabilities", None)
        if cap and cap.data:
            add = cap.inner.get(type_cap, None)
            if add and add.data:
                return add.data
    return []
