from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f325.cloudformation import (
    cfn_iam_has_privileges_over_iam,
    cfn_iam_has_wildcard_resource_on_write_action,
    cfn_iam_is_policy_miss_configured,
    cfn_iam_is_role_over_privileged,
    cfn_kms_key_has_master_keys_exposed_to_everyone,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_kms_key_has_master_keys_exposed_to_everyone(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_wildcard_resource_on_write_action(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_is_policy_miss_configured(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return cfn_iam_is_policy_miss_configured(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_privileges_over_iam(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_is_role_over_privileged(
        content=content, file_ext=file_ext, path=path, template=template
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
                run_cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content, path, template
                ),
                run_cfn_iam_has_wildcard_resource_on_write_action(
                    content, path, template
                ),
                run_cfn_iam_is_policy_miss_configured(
                    content, file_extension, path, template
                ),
                run_cfn_iam_has_privileges_over_iam(content, path, template),
                run_cfn_iam_is_role_over_privileged(
                    content, file_extension, path, template
                ),
            )

    return results
