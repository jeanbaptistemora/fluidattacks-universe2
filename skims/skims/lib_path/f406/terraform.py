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
    iter_aws_efs_file_system,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_aws_efs_unencrypted(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        encrypted = get_attribute(body=resource.data, key="encrypted")
        if not encrypted:
            yield resource
        elif encrypted.val is False:
            yield encrypted


def tfm_aws_efs_unencrypted(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f165.tfm_aws_efs_unencrypted",
        iterator=get_cloud_iterator(
            _tfm_aws_efs_unencrypted(
                resource_iterator=iter_aws_efs_file_system(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_EFS_UNENCRYPTED,
    )
