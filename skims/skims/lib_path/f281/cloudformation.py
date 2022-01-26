from aws.model import (
    AWSElbV2,
    AWSS3BucketPolicy,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_elb2_load_target_groups,
    iter_s3_bucket_policies,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
    policies_iterator: Iterator[Union[AWSS3BucketPolicy, Node]],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            secure_transport = get_node_by_keys(
                statement, ["Condition", "Bool", "aws:SecureTransport"]
            )
            if isinstance(secure_transport, Node) and (
                (effect == "Deny" and secure_transport.raw in TRUE_OPTIONS)
                or (
                    effect == "Allow" and secure_transport.raw in FALSE_OPTIONS
                )
            ):
                yield secure_transport


def _cfn_elb2_uses_insecure_port_iterate_vulnerabilities(
    file_ext: str,
    t_groups_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for t_group in t_groups_iterator:
        safe_ports = (443,)
        port = t_group.raw.get("Port", 80)
        is_port_required = t_group.raw.get("TargetType", "")
        if is_port_required and port not in safe_ports:
            port_node = get_node_by_keys(t_group, ["Port"])
            if isinstance(port_node, Node):
                yield port_node
            else:
                yield AWSElbV2(
                    column=t_group.start_column,
                    data=t_group.data,
                    line=get_line_by_extension(t_group.start_line, file_ext),
                )


#  developer: atrujillo@fluidattacks.com
def cfn_bucket_policy_has_secure_transport(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F281.value.cwe},
        description_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        finding=FindingEnum.F281,
        iterator=get_cloud_iterator(
            _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
    )


#  developer: atrujillo@fluidattacks.com
def cfn_elb2_uses_insecure_port(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F281.value.cwe},
        description_key="src.lib_path.f281.elb2_uses_insecure_port",
        finding=FindingEnum.F281,
        iterator=get_cloud_iterator(
            _cfn_elb2_uses_insecure_port_iterate_vulnerabilities(
                file_ext=file_ext,
                t_groups_iterator=iter_elb2_load_target_groups(
                    template=template
                ),
            )
        ),
        path=path,
    )
