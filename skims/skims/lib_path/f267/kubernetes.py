from collections.abc import (
    Iterator,
)
from kubernetes.structure import (
    get_containers_capabilities,
    get_label_and_data,
    get_pod_spec,
    iter_containers_type,
    iter_security_context,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from utils.function import (
    get_node_by_keys,
)


def _k8s_check_add_capability(
    template: Node,
) -> Iterator[Node]:
    for ctx in iter_security_context(template, True):
        if (cap_add := get_containers_capabilities(ctx, "add")) and cap_add[
            0
        ].data.lower() not in {
            "net_bind_service",
            "null",
            "nil",
            "undefined",
        }:
            yield cap_add[0]


def get_allow_privileges_findings(tag: Node) -> Node | None:
    has_security_context: bool = False
    for node, node_data in tag.data.items():
        if node.data == "securityContext":
            if (
                privileged := node_data.inner.get("allowPrivilegeEscalation")
            ) and privileged.data:
                return privileged
            if not privileged:
                return node
            has_security_context = True

    return tag if not has_security_context else None


def _k8s_allow_privilege_escalation_enabled(
    template: Node,
) -> Iterator[Node]:
    vulns_found: list[Node] = []
    for container in iter_containers_type(template):
        for container_props in container:
            if finding := get_allow_privileges_findings(container_props):
                vulns_found.append(finding)

    yield from vulns_found


def _k8s_check_pod_root_container(template: Node) -> Node | None:
    if (pod_spec := get_pod_spec(template)) and (
        pod_root := get_node_by_keys(
            pod_spec, ["securityContext", "runAsNonRoot"]
        )
    ):
        return pod_root
    return None


def get_container_root_vuln_line(  # NOSONAR
    container_ctx: dict[Node, Node], pod_has_safe_config: bool
) -> Node | None:
    for sec_ctx, ctx_element in container_ctx.items():
        if container_non_root := ctx_element.inner.get("runAsNonRoot"):
            if not container_non_root.data:
                return container_non_root
        elif not pod_has_safe_config:
            return sec_ctx
    return None


def _k8s_check_container_root(
    container_props: Node, pod_has_safe_config: bool
) -> Node | None:
    if container_ctx := get_label_and_data(container_props, "securitycontext"):
        if vuln := get_container_root_vuln_line(
            container_ctx, pod_has_safe_config
        ):
            return vuln
    elif not pod_has_safe_config:
        return container_props
    return None


def _k8s_root_container(
    template: Node,
) -> Iterator[Node]:
    pod_has_safe_config: bool = False
    if (
        pod_root := _k8s_check_pod_root_container(template)
    ) and not pod_root.data:
        yield pod_root
    elif pod_root and pod_root.data:
        pod_has_safe_config = True

    for container in iter_containers_type(template):
        for container_props in container:
            if vuln := _k8s_check_container_root(
                container_props, pod_has_safe_config
            ):
                yield vuln


def get_read_only_findings(tag: Node) -> Node | None:
    has_security_context: bool = False
    for node, node_data in tag.data.items():
        if node.data == "securityContext":
            if (
                read_only := node_data.inner.get("readOnlyRootFilesystem")
            ) and not read_only.data:
                return read_only
            if not read_only:
                return node
            has_security_context = True

    return tag if not has_security_context else None


def _k8s_root_filesystem_read_only(
    template: Node,
) -> Iterator[Node]:
    vulns_found: list[Node] = []
    for container in iter_containers_type(template):
        for container_props in container:
            if finding := get_read_only_findings(container_props):
                vulns_found.append(finding)

    yield from vulns_found


def _k8s_check_run_as_user(
    template: Node,
) -> Iterator[Node]:
    for ctx in iter_security_context(template, False):
        as_user = ctx.inner.get("runAsUser")
        if as_user and as_user.data == 0:
            yield as_user


def _k8s_check_pod_seccomp(template: Node) -> Node | None:
    if (pod_spec := get_pod_spec(template)) and (
        pod_type := get_node_by_keys(
            pod_spec, ["securityContext", "seccompProfile", "type"]
        )
    ):
        return pod_type
    return None


def get_seccomp_vuln_line(  # NOSONAR
    container_ctx: dict[Node, Node], pod_has_safe_config: bool
) -> Node | None:
    for sec_ctx, ctx_element in container_ctx.items():
        if container_seccomp_profile := ctx_element.inner.get(
            "seccompProfile"
        ):
            if container_type := container_seccomp_profile.inner.get("type"):
                if container_type.data:
                    if container_type.data.lower() == "unconfined":
                        return container_type
                elif not pod_has_safe_config:
                    return container_type
            elif not pod_has_safe_config:
                seccomp_node: dict[Node, Node] | None
                if seccomp_node := get_label_and_data(
                    ctx_element, "seccompprofile"
                ):
                    return next(iter(seccomp_node))
        elif not pod_has_safe_config:
            return sec_ctx
    return None


def _k8s_check_container_seccomp(
    container_props: Node, pod_has_safe_config: bool
) -> Node | None:
    if container_ctx := get_label_and_data(container_props, "securitycontext"):
        if vuln := get_seccomp_vuln_line(container_ctx, pod_has_safe_config):
            return vuln
    elif not pod_has_safe_config:
        return container_props
    return None


def _k8s_check_seccomp_profile(
    template: Node,
) -> Iterator[Node]:
    pod_has_safe_config: bool = False

    if (
        (pod_type := _k8s_check_pod_seccomp(template))
        and pod_type.data
        and pod_type.data.lower() == "unconfined"
    ):
        yield pod_type
    elif (
        pod_type
        and pod_type.data
        and pod_type.data.lower()
        in [
            "runtimedefault",
            "localhost",
        ]
    ):
        pod_has_safe_config = True

    for container in iter_containers_type(template):
        for container_props in container:
            if vuln := _k8s_check_container_seccomp(
                container_props, pod_has_safe_config
            ):
                yield vuln


def _k8s_check_privileged_used(
    template: Node,
) -> Iterator[Node]:
    for ctx in iter_security_context(template, True):
        privileged = ctx.inner.get("privileged")
        if privileged and privileged.data:
            yield privileged


def _k8s_check_drop_capability(
    template: Node,
) -> Iterator[Node]:
    for ctx in iter_security_context(template, True):
        cap_drop = get_containers_capabilities(ctx, "drop")
        if cap_drop and "all" not in [cap.data.lower() for cap in cap_drop]:
            yield cap_drop[0]


def _k8s_container_without_securitycontext(
    template: Node,
) -> Iterator[Node]:
    for container in iter_containers_type(template):
        for elem in container:
            if isinstance(elem, Node) and not elem.inner.get(
                "securityContext"
            ):
                yield elem


def k8s_check_add_capability(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_add_capability"),
        iterator=get_cloud_iterator(
            _k8s_check_add_capability(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_CHECK_ADD_CAPABILITY,
    )


def k8s_allow_privilege_escalation_enabled(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f267.k8s_allow_privilege_escalation_enabled"
        ),
        iterator=get_cloud_iterator(
            _k8s_allow_privilege_escalation_enabled(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_PRIVILEGE_ESCALATION_ENABLED,
    )


def k8s_root_container(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_root_container"),
        iterator=get_cloud_iterator(_k8s_root_container(template=template)),
        path=path,
        method=MethodsEnum.K8S_ROOT_CONTAINER,
    )


def k8s_root_filesystem_read_only(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_root_filesystem_read_only"),
        iterator=get_cloud_iterator(
            _k8s_root_filesystem_read_only(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_ROOT_FILESYSTEM_READ_ONLY,
    )


def k8s_check_run_as_user(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_run_as_user"),
        iterator=get_cloud_iterator(_k8s_check_run_as_user(template=template)),
        path=path,
        method=MethodsEnum.K8S_CHECK_RUN_AS_USER,
    )


def k8s_check_seccomp_profile(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_seccomp_profile"),
        iterator=get_cloud_iterator(
            _k8s_check_seccomp_profile(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_CHECK_SECCOMP_PROFILE,
    )


def k8s_check_privileged_used(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_privileged_used"),
        iterator=get_cloud_iterator(
            _k8s_check_privileged_used(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_CHECK_PRIVILEGED_USED,
    )


def k8s_check_drop_capability(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_drop_capability"),
        iterator=get_cloud_iterator(
            _k8s_check_drop_capability(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_CHECK_DROP_CAPABILITY,
    )


def k8s_container_without_securitycontext(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f267.k8s_container_without_securitycontext"
        ),
        iterator=get_cloud_iterator(
            _k8s_container_without_securitycontext(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_CONTAINER_WITHOUT_SECURITYCONTEXT,
    )
