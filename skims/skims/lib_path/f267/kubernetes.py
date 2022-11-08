# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from kubernetes.structure import (
    get_containers_capabilities,
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
from typing import (
    Any,
    Iterator,
    List,
    Union,
)


def _k8s_check_add_capability(
    template: Any,
) -> Iterator[Any]:
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


def _k8s_allow_privilege_escalation_enabled(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
        escalation = ctx.inner.get("allowPrivilegeEscalation")
        if escalation and escalation.data:
            yield escalation
        elif not escalation:
            yield ctx


def _k8s_root_container(
    template: Any,
) -> Iterator[Any]:
    if (
        getattr(template, "raw")
        and hasattr(template.raw, "get")
        and template.raw.get("apiVersion")
        and (ctx := template.inner.get("securityContext"))
    ):
        as_root = ctx.inner.get("runAsNonRoot")
        if as_root and not as_root.data:
            yield as_root
    else:
        for ctx in iter_security_context(template, False):
            as_root = ctx.inner.get("runAsNonRoot")
            if as_root and not as_root.data:
                yield as_root


def get_read_only_findings(tag: Node) -> Union[Node, None]:
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
    vulns_found: List[Node] = []
    for container in iter_containers_type(template):
        for container_props in container:
            if finding := get_read_only_findings(container_props):
                vulns_found.append(finding)

    yield from vulns_found


def _k8s_check_run_as_user(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, False):
        as_user = ctx.inner.get("runAsUser")
        if as_user and as_user.data == 0:
            yield as_user


def _k8s_check_ctx_seccomp(
    ctx: Any,
) -> Iterator[Any]:
    if sec_prof := ctx.inner.get("seccompProfile"):
        if (
            prof_type := sec_prof.inner.get("type")
        ) and prof_type.data.lower() == "unconfined":
            yield prof_type
        elif not sec_prof.inner.get("type"):
            yield sec_prof
    else:
        yield ctx


def _k8s_check_seccomp_profile(
    template: Any,
) -> Iterator[Any]:
    if (
        getattr(template, "raw")
        and hasattr(template.raw, "get")
        and template.raw.get("apiVersion")
        and (ctx := template.inner.get("securityContext"))
    ):
        yield from _k8s_check_ctx_seccomp(ctx)
    else:
        for ctx in iter_security_context(template, False):
            yield from _k8s_check_ctx_seccomp(ctx)


def _k8s_check_privileged_used(
    template: Any,
) -> Iterator[Any]:
    if (
        getattr(template, "raw")
        and hasattr(template.raw, "get")
        and template.raw.get("apiVersion")
        and (ctx := template.inner.get("spec"))
    ):
        privileged = ctx.inner.get("privileged")
        if privileged and privileged.data:
            yield privileged


def _k8s_check_drop_capability(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
        cap_drop = get_containers_capabilities(ctx, "drop")
        if cap_drop and "all" not in [cap.data.lower() for cap in cap_drop]:
            yield cap_drop[0]


def _k8s_container_without_securitycontext(
    template: Any,
) -> Iterator[Any]:
    for container in iter_containers_type(template):
        for elem in container:
            if isinstance(elem, Node) and not elem.inner.get(
                "securityContext"
            ):
                yield elem


def k8s_check_add_capability(
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_root_container"),
        iterator=get_cloud_iterator(_k8s_root_container(template=template)),
        path=path,
        method=MethodsEnum.K8S_ROOT_CONTAINER,
    )


def k8s_root_filesystem_read_only(
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_check_run_as_user"),
        iterator=get_cloud_iterator(_k8s_check_run_as_user(template=template)),
        path=path,
        method=MethodsEnum.K8S_CHECK_RUN_AS_USER,
    )


def k8s_check_seccomp_profile(
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
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
    content: str, path: str, template: Any
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
