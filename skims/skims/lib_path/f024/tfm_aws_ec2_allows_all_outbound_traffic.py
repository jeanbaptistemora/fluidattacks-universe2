from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
)
from parse_hcl2.structure.aws import (
    iter_aws_security_group,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            key="egress",
            body=resource.data,
        ):
            yield resource


def tfm_aws_ec2_allows_all_outbound_traffic(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=(
            "src.lib_path.f024_aws.security_group_without_egress"
        ),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
                resource_iterator=iter_aws_security_group(model=model)
            )
        ),
        path=path,
    )
