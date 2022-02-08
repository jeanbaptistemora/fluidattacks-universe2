from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_aws_s3_versioning_disabled(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if versioning := get_argument(
            body=resource.data,
            key="versioning",
        ):
            versioning_enabled = get_block_attribute(
                block=versioning, key="enabled"
            )
            if versioning_enabled and versioning_enabled.val is False:
                yield versioning_enabled
        else:
            yield resource


def tfm_aws_s3_versioning_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f335.tfm_aws_s3_versioning_disabled"),
        iterator=get_cloud_iterator(
            _tfm_aws_s3_versioning_disabled(
                resource_iterator=iter_s3_buckets(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_S3_VERSIONING_DISABLED,
    )
