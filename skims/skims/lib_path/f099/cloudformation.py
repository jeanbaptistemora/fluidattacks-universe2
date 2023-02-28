from collections.abc import (
    Iterator,
)
from lib_path.common import (
    FALSE_OPTIONS,
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
from parse_cfn.structure import (
    iter_s3_bucket_policies,
)
from typing import (
    Any,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
    policies_iterator: Iterator[Node],
) -> Iterator[Node]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        if not statements:
            continue
        for statement in statements.data:
            effect = (
                statement.raw.get("Effect", "")
                if hasattr(statement, "raw") and hasattr(statement.raw, "get")
                else ""
            )
            sse = get_node_by_keys(
                statement,
                ["Condition", "Null", "s3:x-amz-server-side-encryption"],
            )
            if (
                (
                    sse := get_node_by_keys(
                        statement,
                        [
                            "Condition",
                            "Null",
                            "s3:x-amz-server-side-encryption",
                        ],
                    )
                )
                and (isinstance(sse, Node))
                and (effect == "Allow" and sse.raw in FALSE_OPTIONS)
            ):
                yield sse


def cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f099.bckp_has_server_side_encryption_disabled"
        ),
        iterator=get_cloud_iterator(
            _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_POLICY_SERVER_ENCRYP_DISABLED,
    )
