from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    bucket_policy_allows_public_access_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
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
