from aioextensions import (
    in_process,
)
from aws.model import (
    AWSCloudfrontDistribution,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_line_by_extension,
    get_vulnerabilities_from_aws_iterator_blocking,
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
    iter_cloudfront_distributions,
    iter_s3_buckets,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    get_argument,
    iter_aws_elb,
    iterate_block_attributes,
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
    get_node_by_keys,
    TIMEOUT_1MIN,
)


def _cfn_bucket_has_access_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]],
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        logging = get_node_by_keys(bucket, ["LoggingConfiguration"])
        if not isinstance(logging, Node):
            yield AWSS3Bucket(
                column=bucket.start_column,
                data=bucket.data,
                line=get_line_by_extension(bucket.start_line, file_ext),
            )


def _has_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    distributions_iterator: Iterator[Union[AWSCloudfrontDistribution, Node]],
) -> Iterator[Union[AWSCloudfrontDistribution, Node]]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            logging = get_node_by_keys(dist_config, ["Logging"])
            if not isinstance(logging, Node):
                yield AWSCloudfrontDistribution(
                    column=dist_config.start_column,
                    data=dist_config.data,
                    line=get_line_by_extension(
                        dist_config.start_line, file_ext
                    ),
                )


def tfm_elb_logging_disabled_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        if access_logs := get_argument(body=bucket.data, key="access_logs"):
            for elem in iterate_block_attributes(access_logs):
                if elem.key == "enabled" and elem.val is False:
                    yield elem
        else:
            yield bucket


def _tfm_elb_logging_disabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=core_model.FindingEnum.F200,
        path=path,
        statements_iterator=(
            tfm_elb_logging_disabled_iterate_vulnerabilities(
                buckets_iterator=iter_aws_elb(model=model)
            )
        ),
    )


def _cfn_has_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=core_model.FindingEnum.F200,
        path=path,
        statements_iterator=_has_logging_disabled_iterate_vulnerabilities(
            file_ext=file_ext,
            distributions_iterator=iter_cloudfront_distributions(
                template=template
            ),
        ),
    )


def _cfn_bucket_has_access_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=core_model.FindingEnum.F200,
        path=path,
        statements_iterator=(
            _cfn_bucket_has_access_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_elb_logging_disabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_elb_logging_disabled,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_has_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_has_logging_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_bucket_has_access_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_bucket_has_access_logging_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_has_logging_disabled(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_bucket_has_access_logging_disabled(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_elb_logging_disabled(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
