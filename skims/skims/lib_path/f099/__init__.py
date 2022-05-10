from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f099.cloudformation import (
    cfn_bucket_policy_has_server_side_encryption_disabled,
    cfn_unencrypted_buckets,
)
from lib_path.f099.terraform import (
    tfm_unencrypted_buckets,
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
def run_cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_has_server_side_encryption_disabled(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_unencrypted_buckets(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return cfn_unencrypted_buckets(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_unencrypted_buckets(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag W41 S3 Bucket should have encryption option set
    return tfm_unencrypted_buckets(content=content, path=path, model=model)


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
                run_cfn_bucket_policy_has_server_side_encryption_disabled(
                    content, path, template
                ),
                run_cfn_unencrypted_buckets(
                    content, file_extension, path, template
                ),
            )
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        results = (*results, run_tfm_unencrypted_buckets(content, path, model))

    return results
