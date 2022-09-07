# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f394.cloudformation import (
    cfn_log_files_not_validated,
)
from lib_path.f394.terraform import (
    tfm_trail_log_files_not_validated,
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
def run_cfn_log_files_not_validated(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_log_files_not_validated(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_trail_log_files_not_validated(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_trail_log_files_not_validated(
        content=content, path=path, model=model
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
        results = (
            *results,
            *(
                run_cfn_log_files_not_validated(
                    content, file_extension, path, template
                )
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (run_tfm_trail_log_files_not_validated,)
            ),
        )

    return results
