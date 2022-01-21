from aioextensions import (
    in_process,
)
from aws.model import (
    AWSS3Acl,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets as terraform_iter_s3_buckets,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F080 = core_model.FindingEnum.F080
_FINDING_F080_CWE = _FINDING_F080.value.cwe


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


def _terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F080_CWE},
        description_key="src.lib_path.f080_aws.unencrypted_buckets",
        finding=_FINDING_F080,
        iterator=get_cloud_iterator(
            _public_buckets_iterate_vulnerabilities(
                buckets_iterator=terraform_iter_s3_buckets(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return await in_process(
        _terraform_public_buckets,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            terraform_public_buckets(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
