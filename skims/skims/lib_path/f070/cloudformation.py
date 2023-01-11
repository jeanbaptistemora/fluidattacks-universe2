from aws.model import (
    AWSElbV2,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
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
from parse_cfn.structure import (
    iter_elb2_load_listeners,
    iter_elb2_load_target_groups,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
    listeners_iterator: Iterator[Node],
) -> Iterator[Union[AWSElbV2, Node]]:
    for listener in listeners_iterator:
        ssl_policy = listener.inner.get("SslPolicy")
        if (
            ssl_policy
            and ssl_policy.raw in PREDEFINED_SSL_POLICY_VALUES
            and ssl_policy.raw not in SAFE_SSL_POLICY_VALUES
        ):
            yield ssl_policy


def _cfn_elb2_target_group_insecure_port_iterate_vulnerabilities(
    file_ext: str,
    resources_iterator: Iterator[Node],
) -> Iterator[Union[AWSElbV2, Node]]:
    for target_group in resources_iterator:
        port = target_group.inner.get("Port")
        target_type = (
            target_group.raw.get("TargetType")
            if hasattr(target_group, "raw")
            else ""
        )
        if target_type == "lambda":
            continue
        if not port:
            yield AWSElbV2(
                column=target_group.start_column,
                data=target_group.data,
                line=get_line_by_extension(target_group.start_line, file_ext),
            )
        elif not isinstance(port.raw, dict) and int(port.raw) != 443:
            yield port


def cfn_elb2_uses_insecure_security_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        iterator=get_cloud_iterator(
            _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
                listeners_iterator=iter_elb2_load_listeners(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_ELB2_INSECURE_SEC_POLICY,
    )


def cfn_elb2_target_group_insecure_port(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f070.elb2_target_group_insecure_port",
        iterator=get_cloud_iterator(
            _cfn_elb2_target_group_insecure_port_iterate_vulnerabilities(
                file_ext=file_ext,
                resources_iterator=iter_elb2_load_target_groups(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_LB_TARGET_INSECURE_PORT,
    )
