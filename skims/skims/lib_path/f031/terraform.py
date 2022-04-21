from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    admin_policies_attached_iterate_vulnerabilities,
    bucket_policy_allows_public_access_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
    open_passrole_iterate_vulnerabilities,
    permissive_policy_iterate_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
from typing import (
    Any,
)


def terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(model=model)
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ADMIN_POLICY,
    )


def tfm_bucket_policy_allows_public_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        iterator=get_cloud_iterator(
            bucket_policy_allows_public_access_iterate_vulnerabilities(
                statements_iterator=(
                    terraform_iterate_iam_policy_documents(model=model)
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_BUCKET_ALLOWS_PUBLIC,
    )


def terraform_negative_statement(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.negative_statement",
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_NEGATIVE_STATEMENT,
    )


def terraform_open_passrole(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.open_passrole",
        iterator=get_cloud_iterator(
            open_passrole_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_OPEN_PASSROLE,
    )


def terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031_aws.permissive_policy",
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_PERMISSIVE_POLICY,
    )
