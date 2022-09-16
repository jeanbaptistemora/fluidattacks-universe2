# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.model import (
    AWSEC2,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_ec2_ltemplates_and_instances,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_ec2_has_not_termination_protection_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2 in ec2_iterator:
        ec2_res_data = ec2.inner.get("LaunchTemplateData") or ec2
        if "DisableApiTermination" not in ec2_res_data.raw:  # type: ignore
            yield AWSEC2(
                column=ec2_res_data.start_column,
                data=ec2_res_data.data,
                line=get_line_by_extension(ec2_res_data.start_line, file_ext),
            )
        else:
            dis_api_term = ec2_res_data.inner.get(  # type: ignore
                "DisableApiTermination"
            )
            if dis_api_term.raw in FALSE_OPTIONS:
                yield dis_api_term


def cfn_ec2_has_not_termination_protection(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f257.ec2_has_not_termination_protection",
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_termination_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_ltemplates_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_NOT_TERMINATION_PROTEC,
    )
