from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_JSON,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f325.cloudformation import (
    cfn_iam_allow_wildcard_action_trust_policy,
    cfn_iam_allow_wildcard_actions_perms_policies,
    cfn_iam_has_wildcard_resource_on_write_action,
    cfn_iam_is_policy_actions_wildcards,
    cfn_kms_key_has_master_keys_exposed_to_everyone,
    cfn_permissive_policy,
)
from lib_path.f325.conf_files import (
    json_principal_wildcard,
)
from lib_path.f325.terraform import (
    terraform_permissive_policy,
    tfm_iam_has_wildcard_resource_on_write_action,
    tfm_kms_key_has_master_keys_exposed_to_everyone,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform,
)
from typing import (
    Any,
    Callable,
    Tuple,
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
def run_tfm_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_has_wildcard_resource_on_write_action(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_kms_key_has_master_keys_exposed_to_everyone(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return terraform_permissive_policy(content=content, path=path, model=model)


@SHIELD_BLOCKING
def run_json_principal_wildcard(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_principal_wildcard(
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
                run_cfn_iam_allow_wildcard_actions_perms_policies(
                    content, path, template
                ),
                run_cfn_iam_is_policy_miss_configured(content, path, template),
                run_json_principal_wildcard(content, path, template),
                run_cfn_iam_allow_wildcard_action_trust_policy(
                    content, path, template
                ),
                run_cfn_permissive_policy(content, path, template),
            )
            if file_extension in EXTENSIONS_JSON:
                results = (
                    *results,
                    run_json_principal_wildcard(content, path, template),
                )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (
                    run_tfm_kms_key_has_master_keys_exposed_to_everyone,
                    run_tfm_iam_has_wildcard_resource_on_write_action,
                    run_terraform_permissive_policy,
                )
            ),
        )

    return results
