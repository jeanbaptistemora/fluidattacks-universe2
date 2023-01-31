from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
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
        ssl_policy = get_attribute(body=resource.data, key="ssl_policy")
        if (
            ssl_policy
            and ssl_policy.val in PREDEFINED_SSL_POLICY_VALUES
            and ssl_policy.val not in SAFE_SSL_POLICY_VALUES
        ):
            yield ssl_policy


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
