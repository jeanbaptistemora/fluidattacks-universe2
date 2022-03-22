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
    iter_ec2_instances,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Node],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "IamInstanceProfile" not in ec2_res.inner:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )


def cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f333.ec2_has_not_an_iam_instance_profile"
        ),
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_instances(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_EC2_NO_IAM,
    )
