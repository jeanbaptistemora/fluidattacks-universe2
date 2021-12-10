from aioextensions import (
    in_process,
)
from aws.model import (
    AWSS3Acl,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_aws_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_s3_buckets as cfn_iter_s3_buckets,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets,
)
from parse_hcl2.tokens import (
    Attribute,
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

_FINDING_F335 = core_model.FindingEnum.F335
_FINDING_F335_CWE = _FINDING_F335.value.cwe


def tfm_s3_not_private_access_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    danger_values = {
        "public-read",
        "pulblic-read-write",
        "authenticated-read",
        "bucket-owner-read",
        "bucket-owner-full-control",
        "log-delivery-write",
    }
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "acl"
                and elem.val in danger_values
            ):
                yield elem


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


def _tfm_s3_not_private_access(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F335_CWE},
        description_key="F335.title",
        finding=_FINDING_F335,
        iterator=get_aws_iterator(
            tfm_s3_not_private_access_iterate_vulnerabilities(
                buckets_iterator=iter_s3_buckets(model=model)
            )
        ),
        path=path,
    )


def _cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F335_CWE},
        description_key="F335.title",
        finding=_FINDING_F335,
        iterator=get_aws_iterator(
            _public_buckets_iterate_vulnerabilities(
                buckets_iterator=cfn_iter_s3_buckets(template=template)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return await in_process(
        _cfn_public_buckets,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_s3_not_private_access(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_s3_not_private_access,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_s3_not_private_access(
                content=content,
                path=path,
                model=model,
            )
        )
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_public_buckets(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    return coroutines
