from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f267.kubernetes import (
    k8s_allow_privilege_escalation_enabled,
    k8s_root_container,
    k8s_root_filesystem_read_only,
    k8s_sys_admin_or_privileged_used,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_k8s_sys_admin_or_privileged_used(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_sys_admin_or_privileged_used(
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
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_k8s_sys_admin_or_privileged_used(content, path, template),
                run_k8s_allow_privilege_escalation_enabled(
                    content, path, template
                ),
                run_k8s_root_container(content, path, template),
                run_k8s_root_filesystem_read_only(content, path, template),
            )
    return results
