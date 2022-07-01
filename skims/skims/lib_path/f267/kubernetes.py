from kubernetes.structure import (
    get_containers_capabilities,
    is_kubernetes,
    is_privileged,
    iter_containers_type,
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
    if is_kubernetes(template):
        for container_type in iter_containers_type(template):
            for container in container_type:
                for cap in get_containers_capabilities(container, "add"):
                    if cap.data == "SYS_ADMIN":
                        yield cap
                if privileged := is_privileged(container):
                    print(privileged)
                    yield privileged


def _k8s_allow_privilege_escalation_enabled(
    template: Any,
) -> Iterator[Any]:
    if is_kubernetes(template):
        for container in iter_containers_type(template):
            for elem in container:
                sec_cont = (
                    elem.inner.get("securityContext", None)
                    if elem and elem.data
                    else None
                )
                if sec_cont and sec_cont.data:
                    escalation = sec_cont.inner.get(
                        "allowPrivilegeEscalation", None
                    )
                    if escalation and escalation.data:
                        yield escalation
                    elif not escalation:
                        yield elem


def _k8s_root_container(
    template: Any,
) -> Iterator[Any]:
    if is_kubernetes(template):
        for container in iter_containers_type(template):
            for elem in container:
                sec_cont = (
                    elem.inner.get("securityContext", None)
                    if elem and elem.data
                    else None
                )
                if sec_cont and sec_cont.data:
                    as_root = sec_cont.inner.get("runAsNonRoot", None)
                    if as_root and not as_root.data:
                        yield as_root


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
