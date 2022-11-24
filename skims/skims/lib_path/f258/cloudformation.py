from aws.model import (
    AWSElbV2,
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
    iter_elb2_load_balancers,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_elb2_has_not_deletion_protection_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Node],
) -> Iterator[Union[AWSElbV2, Node]]:
    for elb in load_balancers_iterator:
        attrs = get_node_by_keys(elb, ["LoadBalancerAttributes"])
        if not isinstance(attrs, Node):
            yield AWSElbV2(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        else:
            key_vals = [
                attr
                for attr in attrs.data
                if attr.raw["Key"] == "deletion_protection.enabled"
            ]
            if key_vals:
                key = key_vals[0]
                if key.raw["Value"] in FALSE_OPTIONS:
                    yield key.inner["Value"]
            else:
                yield AWSElbV2(
                    column=attrs.start_column,
                    data=attrs.data,
                    line=get_line_by_extension(attrs.start_line, file_ext),
                )


def cfn_elb2_has_not_deletion_protection(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f258.elb2_has_not_deletion_protection",
        iterator=get_cloud_iterator(
            _cfn_elb2_has_not_deletion_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb2_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ELB2_NOT_DELETION_PROTEC,
    )
