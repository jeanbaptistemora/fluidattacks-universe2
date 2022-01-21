from aws.model import (
    AWSS3Acl,
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
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets as terraform_iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _public_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]]
) -> Iterator[Union[AWSS3Acl, Node]]:
    for bucket in buckets_iterator:
        if isinstance(bucket, Node):
            if bucket.raw.get("AccessControl", "Private") == "PublicReadWrite":
                yield bucket.inner["AccessControl"]
        elif isinstance(bucket, AWSS3Bucket):
            acl = get_attribute(body=bucket.data, key="acl")
            if acl and acl.val == "public-read-write":
                yield AWSS3Acl(
                    data=acl.val,
                    column=acl.column,
                    line=acl.line,
                )


def terraform_public_buckets(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F080.value.cwe},
        description_key="src.lib_path.f080_aws.public_buckets",
        finding=FindingEnum.F080,
        iterator=get_cloud_iterator(
            _public_buckets_iterate_vulnerabilities(
                buckets_iterator=terraform_iter_s3_buckets(model=model)
            )
        ),
        path=path,
    )
