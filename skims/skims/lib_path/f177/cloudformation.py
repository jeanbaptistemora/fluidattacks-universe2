from aws.model import (
    AWSEC2,
)
from lib_path.common import (
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

SECURITY_GROUP_ATTRIBUTES = {"SecurityGroups", "SecurityGroupIds"}


def _cfn_ec2_use_default_security_group_iterate_vulnerabilities(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[Union[AWSEC2, Node]]:
    for res in res_iterator:
        res = (
            lt_data
            if (lt_data := res.inner.get("LaunchTemplateData"))
            else res
        )
        if hasattr(res, "raw") and not any(
            attr in res.raw for attr in SECURITY_GROUP_ATTRIBUTES
        ):
            yield AWSEC2(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )


def cfn_ec2_use_default_security_group(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f177.ec2_using_default_security_group",
        iterator=get_cloud_iterator(
            _cfn_ec2_use_default_security_group_iterate_vulnerabilities(
                file_ext=file_ext,
                res_iterator=iter_ec2_ltemplates_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_DEFAULT_SEC_GROUP,
    )
