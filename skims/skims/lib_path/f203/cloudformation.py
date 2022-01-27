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
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_public_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        if bucket.raw.get("AccessControl", "Private") == "PublicReadWrite":
            yield bucket.inner["AccessControl"]


def cfn_public_buckets(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F203.value.cwe},
        description_key="src.lib_path.f203.public_buckets",
        finding=FindingEnum.F203,
        iterator=get_cloud_iterator(
            _cfn_public_buckets_iterate_vulnerabilities(
                buckets_iterator=iter_s3_buckets(template=template)
            )
        ),
        path=path,
        developer=DeveloperEnum.ANDRES_CUBEROS,
    )
