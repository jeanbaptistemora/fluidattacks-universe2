from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f099.cloudformation import (
    cfn_bucket_policy_has_server_side_encryption_disabled,
    cfn_unencrypted_buckets,
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
                run_cfn_bucket_policy_has_server_side_encryption_disabled(
                    content, path, template
                ),
                run_cfn_unencrypted_buckets(
                    content, file_extension, path, template
                ),
            )

    return results
