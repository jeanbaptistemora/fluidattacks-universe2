from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_lb_target_group,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        port = get_attribute(body=resource.data, key="port")
        if not port:
            yield resource
        elif isinstance(port.val, int) and port.val != 443:
            yield port


def tfm_lb_target_group_insecure_port(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        iterator=get_cloud_iterator(
            _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
                resource_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_LB_TARGET_INSECURE_PORT,
    )
