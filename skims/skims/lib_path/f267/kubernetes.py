from kubernetes.structure import (
    get_containers,
    get_containers_capabilities,
    is_kubernetes,
    is_privileged,
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
        for cap in get_containers_capabilities(template, "add"):
            if cap.data == "SYS_ADMIN":
                yield cap
        privileged = is_privileged(template)
        if privileged and privileged.data:
            yield privileged


def _k8s_allow_privilege_escalation_enabled(
    template: Any,
) -> Iterator[Any]:
    if is_kubernetes(template):
        containers = get_containers(template)
        for elem in containers:
            if elem and elem.data:
                sec_cont = elem.inner.get("securityContext", None)
                if sec_cont and sec_cont.data:
                    escalation = sec_cont.inner.get(
                        "allowPrivilegeEscalation", None
                    )
                    if escalation and escalation.data:
                        yield escalation
                    elif not escalation:
                        yield elem


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
