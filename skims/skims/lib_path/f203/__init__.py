# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f203.cloudformation import (
    cfn_public_buckets,
)
from lib_path.f203.terraform import (
    tfm_public_buckets,
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
def run_cfn_public_buckets(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return cfn_public_buckets(content=content, path=path, template=template)


@SHIELD_BLOCKING
def run_tfm_public_buckets(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_public_buckets(
        content=content,
        path=path,
        model=model,
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
        results = (
            *results,
            *(
                run_cfn_public_buckets(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        results = (*results, run_tfm_public_buckets(content, path, model))

    return results
