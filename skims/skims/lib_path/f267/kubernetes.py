from kubernetes.structure import (
    get_containers_capabilities,
    is_kubernetes,
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


def _k8s_sys_admin_linux_cap_is_used(
    template: Any,
) -> Iterator[Any]:
    if is_kubernetes(template):
        for cap in get_containers_capabilities(template, "add"):
            if cap.data == "SYS_ADMIN":
                yield cap


def k8s_sys_admin_linux_cap_used(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f267.k8s_sys_admin_linux_cap_is_used"),
        iterator=get_cloud_iterator(
            _k8s_sys_admin_linux_cap_is_used(template=template)
        ),
        path=path,
        method=MethodsEnum.CFN_NOT_POINT_TIME_RECOVERY,
    )
