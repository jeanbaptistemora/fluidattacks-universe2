from aws.model import (
    AWSIamManagedPolicy,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    bucket_policy_allows_public_access_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
)
from typing import (
    Any,
)


def _iam_yield_full_access_ssm_vuln(
    action: Any,
) -> Iterator[AWSIamManagedPolicy | Node]:
    if hasattr(action, "raw") and isinstance(action.raw, list):
        for act in action.data:
            if hasattr(act, "raw") and act.raw == "ssm:*":
                yield act
    else:
        if hasattr(action, "raw") and action.raw == "ssm:*":
            yield action


def _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
    iam_iterator: Iterator[Node],
) -> Iterator[AWSIamManagedPolicy | Node]:
    for stmt in iam_iterator:
        effect = stmt.inner.get("Effect")
        action = stmt.inner.get("Action")
        if (
            effect
            and hasattr(effect, "raw")
            and action
            and effect.raw == "Allow"
        ):
            yield from _iam_yield_full_access_ssm_vuln(action)


def cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        iterator=get_cloud_iterator(
            bucket_policy_allows_public_access_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_BUCKET_ALLOWS_PUBLIC,
    )


def cfn_negative_statement(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.negative_statement",
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_NEGATIVE_STATEMENT,
    )


def cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        iterator=get_cloud_iterator(
            _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                iam_iterator=cfn_iterate_iam_policy_documents(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_IAM_FULL_ACCESS_SSM,
    )
