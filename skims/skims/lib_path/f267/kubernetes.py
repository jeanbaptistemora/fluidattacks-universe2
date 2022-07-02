from kubernetes.structure import (
    get_containers_capabilities,
    iter_security_context,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
)


def _k8s_sys_admin_or_privileged_used(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
        for cap in get_containers_capabilities(ctx, "add"):
            if cap.data == "SYS_ADMIN":
                yield cap
        privileged = ctx.inner.get("privileged")
        if privileged and privileged.data:
            yield privileged


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
    if template.raw.get("apiVersion") and (
        ctx := template.inner.get("securityContext")
    ):
        as_root = ctx.inner.get("runAsNonRoot")
        if as_root and not as_root.data:
            yield as_root
    else:
        for ctx in iter_security_context(template, False):
            as_root = ctx.inner.get("runAsNonRoot")
            if as_root and not as_root.data:
                yield as_root


def _k8s_root_filesystem_read_only(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, False):
        read_only = ctx.inner.get("readOnlyRootFilesystem")
        if read_only and not read_only.data:
            yield read_only
        elif not read_only:
            yield ctx


def k8s_sys_admin_or_privileged_used(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_sys_admin_linux_cap_is_used"),
        iterator=get_cloud_iterator(
            _k8s_sys_admin_or_privileged_used(template=template)
        ),
        path=path,
        method=MethodsEnum.K8S_SYS_ADMIN_LINUX_CAP_USED,
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
