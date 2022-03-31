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
    iter_aws_secrets_manager_secret,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_aws_secret_encrypted_whitouth_kms_cmk(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_attribute(
            key="kms_key_id",
            body=resource.data,
        ):
            yield resource


def tfm_aws_secret_encrypted_whitouth_kms_cmk(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f411.tfm_aws_secret_encrypted_whitouth_kms_cmk"
        ),
        iterator=get_cloud_iterator(
            _tfm_aws_secret_encrypted_whitouth_kms_cmk(
                resource_iterator=iter_aws_secrets_manager_secret(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_SECRET_WHITOUTH_KMS_CMK,
    )
