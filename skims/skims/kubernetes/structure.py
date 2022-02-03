from metaloaders.model import (
    Node,
)
from typing import (
    Optional,
)


def is_kubernetes(template: Node) -> bool:
    if template and template.data and isinstance(template.inner, dict):
        if (
            list(template.inner.keys())
            and list(template.inner.keys())[0] == "apiVersion"
        ):
            return True
    return False


def is_privileged(template: Node) -> Optional[Node]:
    if template and template.data:
        k8s_spec = template.inner.get("spec", None)
        if k8s_spec and k8s_spec.data:
            privileged = k8s_spec.inner.get("privileged")
            if privileged:
                return privileged
    return None


def get_containers(
    template: Node,
) -> list:
    if template and template.data:
        k8s_spec = template.inner.get("spec", None)
        if k8s_spec and k8s_spec.data:
            containers = k8s_spec.inner.get("containers", None)
            if containers and containers.data:
                return containers.data
    return []


def get_containers_images(
    template: Node,
) -> list:
    containers = get_containers(template)
    if containers and isinstance(containers, list):
        images = [
            container.inner["image"]
            for container in get_containers(template)
            if (container.data and container.inner.get("image", None))
        ]
        return images
    return []


def get_containers_capabilities(template: Node, type_cap: str) -> list:
    containers = get_containers(template)
    for elem in containers:
        if elem and elem.data:
            sec_cont = elem.inner.get("securityContext", None)
            if sec_cont and sec_cont.data:
                cap = sec_cont.inner.get("capabilities", None)
                if cap and cap.data:
                    add = cap.inner.get(type_cap, None)
                    if add and add.data:
                        return add.data
    return []
