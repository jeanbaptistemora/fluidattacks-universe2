from aws.model import (
    AWSS3BucketPolicy,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_s3_bucket_policies,
)
from typing import (
    Any,
    Iterator,
    Optional,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def aux_cfn_bucket_policy(
    secure_transport: Optional[Node], effect: str
) -> bool:
    if isinstance(secure_transport, Node) and (
        (effect == "Deny" and secure_transport.raw in TRUE_OPTIONS)
        or (effect == "Allow" and secure_transport.raw in FALSE_OPTIONS)
    ):
        return True
    return False


def _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
    policies_iterator: Iterator[Node],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        if not statements:
            continue
        for statement in statements.data:
            effect = (
                statement.raw.get("Effect")
                if hasattr(statement, "raw") and hasattr(statement.raw, "get")
                else ""
            )
            secure_transport = get_node_by_keys(
                statement, ["Condition", "Bool", "aws:SecureTransport"]
            )
            if isinstance(secure_transport, Node) and aux_cfn_bucket_policy(
                secure_transport, effect
            ):
                yield secure_transport


def cfn_bucket_policy_has_secure_transport(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        iterator=get_cloud_iterator(
            _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_BUCKET_POLICY_SEC_TRANSPORT,
    )
