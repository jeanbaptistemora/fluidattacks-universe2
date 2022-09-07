# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.model import (
    AWSCTrail,
)
from lib_path.common import (
    FALSE_OPTIONS,
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
from parse_hcl2.structure.aws import (
    iter_aws_cloudtrail,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_trail_log_files_not_validated_iter_vulns(
    resource_iterator: Iterator[AWSCTrail],
) -> Iterator[Union[Attribute, AWSCTrail]]:
    for res in resource_iterator:
        log_file_val = get_attribute(res.data, "enable_log_file_validation")
        if log_file_val is None:
            yield res
        elif log_file_val.val in FALSE_OPTIONS:
            yield log_file_val


def tfm_trail_log_files_not_validated(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f394.tfm_log_files_not_validated"),
        iterator=get_cloud_iterator(
            _tfm_trail_log_files_not_validated_iter_vulns(
                resource_iterator=iter_aws_cloudtrail(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_CTRAIL_LOG_NOT_VALIDATED,
    )
