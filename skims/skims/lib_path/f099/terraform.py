from aws.model import (
    AWSS3Bucket,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets as tfm_iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_unencrypted_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if not bucket.raw.get("BucketEncryption", None):
                yield bucket
        elif isinstance(bucket, AWSS3Bucket) and not get_argument(
            key="server_side_encryption_configuration",
            body=bucket.data,
        ):
            yield bucket


def tfm_unencrypted_buckets(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F099.value.cwe},
        description_key="src.lib_path.f099.unencrypted_buckets",
        finding=FindingEnum.F099,
        iterator=get_cloud_iterator(
            _tfm_unencrypted_buckets_iterate_vulnerabilities(
                buckets_iterator=tfm_iter_s3_buckets(model=model)
            )
        ),
        path=path,
    )
