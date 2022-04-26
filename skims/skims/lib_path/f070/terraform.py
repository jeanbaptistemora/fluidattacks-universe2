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
    iter_aws_elb2_listener,
    iter_aws_lb_target_group,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        acceptable = (
            "ELBSecurityPolicy-2016-08",
            "ELBSecurityPolicy-TLS-1-1-2017-01",
            "ELBSecurityPolicy-FS-2018-06",
            "ELBSecurityPolicy-TLS-1-2-Ext-2018-06",
        )
        ssl_policy = get_attribute(body=resource.data, key="ssl_policy")
        if ssl_policy and ssl_policy.val not in acceptable:
            yield ssl_policy


def _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        port = get_attribute(body=resource.data, key="port")
        if not port:
            yield resource
        elif isinstance(port.val, int) and port.val != 443:
            yield port


def tfm_elb2_uses_insecure_security_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        iterator=get_cloud_iterator(
            _tfm_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
                resource_iterator=iter_aws_elb2_listener(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ELB2_INSECURE_SEC_POLICY,
    )


def tfm_lb_target_group_insecure_port(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f070.elb2_target_group_insecure_port",
        iterator=get_cloud_iterator(
            _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
                resource_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_LB_TARGET_INSECURE_PORT,
    )
