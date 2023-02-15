from aws.model import (
    AWSIamPolicyStatement,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iter_aws_s3_bucket_policy_statements,
)
from typing import (
    Any,
)
from utils.function import (
    get_dict_values,
)


def _tfm_bucket_policy_has_secure_transport_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in stmts_iterator:
        effect = stmt.data.get("Effect")
        secure_transport = get_dict_values(
            stmt.data, "Condition", "Bool", "aws:SecureTransport"
        )
        if secure_transport and (
            (effect == "Deny" and secure_transport in TRUE_OPTIONS)
            or (effect == "Allow" and secure_transport in FALSE_OPTIONS)
        ):
            yield stmt


def tfm_bucket_policy_has_secure_transport(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f281.bucket_policy_has_secure_transport"
        ),
        iterator=get_cloud_iterator(
            _tfm_bucket_policy_has_secure_transport_iter_vulns(
                stmts_iterator=iter_aws_s3_bucket_policy_statements(
                    model=model
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_BUCKET_POLICY_SEC_TRANSPORT,
    )
