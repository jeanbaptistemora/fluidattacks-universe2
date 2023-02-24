from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f325.cloudformation import (
    cfn_iam_allow_wildcard_action_trust_policy,
    cfn_iam_allow_wildcard_actions_perms_policies,
    cfn_iam_has_wildcard_resource_on_trust_policies,
    cfn_iam_has_wildcard_resource_on_write_action,
    cfn_iam_is_policy_actions_wildcards,
    cfn_kms_key_has_master_keys_exposed_to_everyone,
    cfn_permissive_policy,
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
def run_cfn_permissive_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_permissive_policy(content=content, path=path, template=template)


@SHIELD_BLOCKING
def run_cfn_iam_allow_wildcard_actions_perms_policies(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_wildcard_actions_perms_policies(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_allow_wildcard_action_trust_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_wildcard_action_trust_policy(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_kms_key_has_master_keys_exposed_to_everyone(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_has_wildcard_resource_on_trust_policies(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_wildcard_resource_on_trust_policies(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_wildcard_resource_on_write_action(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_is_policy_miss_configured(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return cfn_iam_is_policy_actions_wildcards(
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

    content = content_generator()

    if file_extension in EXTENSIONS_CLOUDFORMATION:

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content, path, template
                ),
                run_cfn_iam_has_wildcard_resource_on_write_action(
                    content, path, template
                ),
                run_cfn_iam_has_wildcard_resource_on_trust_policies(
                    content, path, template
                ),
                run_cfn_iam_allow_wildcard_actions_perms_policies(
                    content, path, template
                ),
                run_cfn_iam_is_policy_miss_configured(content, path, template),
                run_cfn_iam_allow_wildcard_action_trust_policy(
                    content, path, template
                ),
                run_cfn_permissive_policy(content, path, template),
            )

    return results
