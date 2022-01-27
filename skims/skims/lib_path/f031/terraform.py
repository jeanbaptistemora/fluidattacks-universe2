from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f031.utils import (
    admin_policies_attached_iterate_vulnerabilities,
    negative_statement_iterate_vulnerabilities,
    open_passrole_iterate_vulnerabilities,
    permissive_policy_iterate_vulnerabilities,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_instance,
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_attribute(
            key="iam_instance_profile",
            body=resource.data,
        ):
            yield resource


def terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(model=model)
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.ANDRES_CUBEROS,
    )


def terraform_negative_statement(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.negative_statement",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            negative_statement_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.ANDRES_CUBEROS,
    )


def terraform_open_passrole(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.open_passrole",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            open_passrole_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.ANDRES_CUBEROS,
    )


def terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.ANDRES_CUBEROS,
    )


def tfm_ec2_has_not_an_iam_instance_profile(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F031.value.cwe},
        description_key=(
            "src.lib_path.f031.ec2_has_not_an_iam_instance_profile"
        ),
        finding=FindingEnum.F031,
        iterator=get_cloud_iterator(
            _tfm_ec2_has_not_an_iam_instance_profile_iterate_vulnerabilities(
                resource_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )
