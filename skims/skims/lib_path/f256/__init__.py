# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f256.cloudformation import (
    cfn_rds_has_not_automated_backups,
    cfn_rds_has_not_termination_protection,
)
from lib_path.f256.terraform import (
    tfm_db_has_not_automated_backups,
    tfm_db_no_deletion_protection,
    tfm_rds_has_not_automated_backups,
    tfm_rds_no_deletion_protection,
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
def run_cfn_rds_has_not_automated_backups(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_rds_has_not_automated_backups(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_rds_has_not_termination_protection(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_rds_has_not_termination_protection(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_db_no_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_db_no_deletion_protection(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_rds_no_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_rds_no_deletion_protection(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_db_has_not_automated_backups(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_db_has_not_automated_backups(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_rds_has_not_automated_backups(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_rds_has_not_automated_backups(
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

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_rds_has_not_automated_backups(content, path, template),
                run_cfn_rds_has_not_termination_protection(
                    content, file_extension, path, template
                ),
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            run_tfm_db_no_deletion_protection(content, path, model),
            run_tfm_rds_no_deletion_protection(content, path, model),
            run_tfm_db_has_not_automated_backups(content, path, model),
            run_tfm_rds_has_not_automated_backups(content, path, model),
        )

    return results
