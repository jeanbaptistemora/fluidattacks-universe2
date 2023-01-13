from aws.model import (
    AWSIamRole,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    _yield_statements_from_policy_document_attribute,
    iter_aws_iam_role,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
)


def _check_assume_role_policies(assume_role_policy: Attribute) -> bool:
    for stmt in _yield_statements_from_policy_document_attribute(
        assume_role_policy
    ):
        effect = stmt.data.get("Effect")
        if effect == "Allow" and stmt.data.get("NotPrincipal"):
            return True
    return False


def _tfm_iam_role_is_over_privileged_iter_vulns(
    role_iterator: Iterator[AWSIamRole],
) -> Iterator[Any]:
    for res in role_iterator:
        assume_role_policy = get_attribute(res.data, "assume_role_policy")
        if assume_role_policy and _check_assume_role_policies(
            assume_role_policy
        ):
            yield assume_role_policy


def tfm_iam_role_is_over_privileged(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f165.iam_allow_not_principal_trust_policy"
        ),
        iterator=get_cloud_iterator(
            _tfm_iam_role_is_over_privileged_iter_vulns(
                role_iterator=iter_aws_iam_role(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_ROLE_OVER_PRIVILEGED,
    )
