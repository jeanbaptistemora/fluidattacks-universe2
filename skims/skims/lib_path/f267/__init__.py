from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f267.kubernetes import (
    k8s_allow_privilege_escalation_enabled,
    k8s_check_add_capability,
    k8s_check_drop_capability,
    k8s_check_privileged_used,
    k8s_check_run_as_user,
    k8s_check_seccomp_profile,
    k8s_container_without_securitycontext,
    k8s_root_container,
    k8s_root_filesystem_read_only,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_k8s_check_add_capability(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_add_capability(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_allow_privilege_escalation_enabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_allow_privilege_escalation_enabled(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_root_container(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_root_container(content=content, path=path, template=template)


@SHIELD_BLOCKING
def run_k8s_root_filesystem_read_only(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_root_filesystem_read_only(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_check_run_as_user(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_run_as_user(content=content, path=path, template=template)


@SHIELD_BLOCKING
def run_k8s_check_seccomp_profile(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_seccomp_profile(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_check_privileged_used(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_privileged_used(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_check_drop_capability(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_drop_capability(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_k8s_container_without_securitycontext(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_container_without_securitycontext(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:

    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_k8s_check_add_capability(content, path, template),
                run_k8s_allow_privilege_escalation_enabled(
                    content, path, template
                ),
                run_k8s_root_container(content, path, template),
                run_k8s_root_filesystem_read_only(content, path, template),
                run_k8s_check_run_as_user(content, path, template),
                run_k8s_check_seccomp_profile(content, path, template),
                run_k8s_check_privileged_used(content, path, template),
                run_k8s_check_drop_capability(content, path, template),
                run_k8s_container_without_securitycontext(
                    content, path, template
                ),
            )
    return results
