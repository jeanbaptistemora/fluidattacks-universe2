# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.terraform import (
    iter_terraform_settings,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_check_required_version(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_attribute(resource.data, "required_version"):
            yield resource


def tfm_check_required_version(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f381.tfm_check_required_version"),
        iterator=get_cloud_iterator(
            _tfm_check_required_version(
                resource_iterator=iter_terraform_settings(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.CHECK_REQUIRED_VERSION,
    )
