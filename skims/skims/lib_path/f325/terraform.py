from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f325.utils import (
    permissive_policy_iterate_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents,
)
from typing import (
    Any,
)


def terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f325_aws.permissive_policy",
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_PERMISSIVE_POLICY,
    )
