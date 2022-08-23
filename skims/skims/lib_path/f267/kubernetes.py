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


def _k8s_check_add_capability(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
        if (
            cap_add := get_containers_capabilities(ctx, "add")
        ) and not cap_add[0].data.lower() in {
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


def _k8s_root_filesystem_read_only(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
        read_only = ctx.inner.get("readOnlyRootFilesystem")
        if read_only and not read_only.data:
            yield read_only
        elif not read_only:
            yield ctx


def _k8s_check_run_as_user(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, False):
        as_user = ctx.inner.get("runAsUser")
        if as_user and as_user.data == 0:
            yield as_user


def _k8s_check_seccomp_profile(
    template: Any,
) -> Iterator[Any]:
    if (
        getattr(template, "raw")
        and template.raw.get("apiVersion")
        and (ctx := template.inner.get("securityContext"))
    ):
        if sec_prof := ctx.inner.get("seccompProfile"):
            if (
                prof_type := sec_prof.inner.get("type")
            ) and prof_type.data.lower() == "unconfined":
                yield prof_type
            elif not sec_prof.inner.get("type"):
                yield sec_prof
        else:
            yield ctx
    else:
        for ctx in iter_security_context(template, False):
            if sec_prof := ctx.inner.get("seccompProfile"):
                if (
                    prof_type := sec_prof.inner.get("type")
                ) and prof_type.data.lower() == "unconfined":
                    yield prof_type
                elif not sec_prof.inner.get("type"):
                    yield sec_prof
            else:
                yield ctx


def _k8s_check_privileged_used(
    template: Any,
) -> Iterator[Any]:
    for ctx in iter_security_context(template, True):
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
