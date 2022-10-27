# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.model import (
    AWSS3Bucket,
    AWSS3VersionConfig,
    S3VersioningEnum,
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
    get_argument,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets,
    iter_s3_version_configuration,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    List,
    Union,
)


def _s3_has_versioning(
    bucket: AWSS3Bucket,
    versioning_configs: List[AWSS3VersionConfig],
) -> bool:
    for versioning_config in versioning_configs:
        if (
            bucket.name is not None
            and bucket.tf_reference is not None
            and (
                versioning_config.bucket
                in (bucket.name, f"{bucket.tf_reference}.id")
            )
            and versioning_config.status == S3VersioningEnum.ENABLED
        ):
            return True
    return False


def _tfm_aws_s3_versioning_disabled(
    bucket_iterator: Iterator[AWSS3Bucket],
    versioning_iterator: Iterator[AWSS3VersionConfig],
) -> Iterator[Union[AWSS3Bucket, Attribute]]:
    versioning_configs = list(versioning_iterator)
    for bucket in bucket_iterator:
        if versioning := get_argument(
            body=bucket.data,
            key="versioning",
        ):
            versioning_enabled = get_block_attribute(
                block=versioning, key="enabled"
            )
            if versioning_enabled and versioning_enabled.val is False:
                yield versioning_enabled
        elif not _s3_has_versioning(bucket, versioning_configs):
            yield bucket


def tfm_aws_s3_versioning_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f335.tfm_aws_s3_versioning_disabled"),
        iterator=get_cloud_iterator(
            _tfm_aws_s3_versioning_disabled(
                bucket_iterator=iter_s3_buckets(model=model),
                versioning_iterator=iter_s3_version_configuration(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AWS_S3_VERSIONING_DISABLED,
    )
