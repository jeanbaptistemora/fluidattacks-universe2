from collections.abc import (
    Iterator,
)
from metaloaders.model import (
    Node,
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
        "initContainers",
    }
    if check_template_integrity(template) and template.data:
        k8s_spec = template.inner.get("spec", None)
        if k8s_spec and k8s_spec.data:
            for c_type in containers_type:
                if container := k8s_spec.inner.get(c_type, None):
                    yield container.data


def get_containers_capabilities(sec_ctx: Node, type_cap: str) -> list:
    cap = sec_ctx.inner.get("capabilities")
    if cap and cap.data:
        add = cap.inner.get(type_cap, None)
        if add and add.data:
            return add.data
    return []


def check_template_integrity(template: Node) -> bool:
    return bool(
        template
        and hasattr(template, "raw")
        and hasattr(template.raw, "get")
        and template.raw.get("apiVersion")
    )


def iter_security_context(
    template: Node, container_only: bool
) -> Iterator[Node]:
    if check_template_integrity(template):
        if (
            not container_only
            and (kind := template.inner.get("kind"))
            and kind.data == "Pod"
        ):
            spec = template.inner.get("spec")
            if spec and (sec_ctx := spec.inner.get("securityContext")):
                yield sec_ctx if sec_ctx and sec_ctx.data else spec
        for container in iter_containers_type(template):
            for elem in container:
                ctx = elem.inner.get("securityContext")
                yield ctx if ctx and ctx.data else elem


def get_pod_spec(template: Node) -> Node | None:
    if (
        check_template_integrity(template)
        and (kind := template.inner.get("kind"))
        and kind.data == "Pod"
        and (spec := template.inner.get("spec"))
    ):
        return spec
    return None


def get_label_and_data(template: Node, label: str) -> dict[Node, Node] | None:
    for label_tag, data in template.data.items():
        if (
            label_tag.data
            and isinstance(label_tag.data, str)
            and label_tag.data.lower() == label
        ):
            return {label_tag: data}
    return None
