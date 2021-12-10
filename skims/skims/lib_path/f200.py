from aioextensions import (
    in_process,
)
from aws.model import (
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSElb,
    AWSElbV2,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    FALSE_OPTIONS,
    get_aws_iterator,
    get_line_by_extension,
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
    iter_cloudfront_distributions,
    iter_cloudtrail_trail,
    iter_elb2_load_balancers,
    iter_elb_load_balancers,
    iter_s3_buckets,
)
from parse_hcl2.common import (
    get_argument,
    iterate_block_attributes,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_elb,
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

_FINDING_F200 = core_model.FindingEnum.F200
_FINDING_F200_CWE = _FINDING_F200.value.cwe


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


def _cfn_trails_not_multiregion_iterate_vulnerabilities(
    file_ext: str,
    trails_iterator: Iterator[Union[AWSCTrail, Node]],
) -> Iterator[Union[AWSCTrail, Node]]:
    for trail in trails_iterator:
        multi_reg = get_node_by_keys(trail, ["IsMultiRegionTrail"])
        if not isinstance(multi_reg, Node):
            yield AWSCTrail(
                column=trail.start_column,
                data=trail.data,
                line=get_line_by_extension(trail.start_line, file_ext),
            )
        elif multi_reg.raw in FALSE_OPTIONS:
            yield multi_reg


def _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Union[AWSElb, Node]],
) -> Iterator[Union[AWSElb, Node]]:
    for elb in load_balancers_iterator:
        access_log = get_node_by_keys(elb, ["AccessLoggingPolicy", "Enabled"])
        if not isinstance(access_log, Node):
            yield AWSElb(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        elif access_log.raw in FALSE_OPTIONS:
            yield access_log


def _cfn_elb2_has_access_logs_s3_disabled_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for elb in load_balancers_iterator:
        attrs = get_node_by_keys(elb, ["LoadBalancerAttributes"])
        if not isinstance(attrs, Node):
            yield AWSElbV2(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        else:
            key_vals = [
                attr
                for attr in attrs.data
                if attr.raw["Key"] == "access_logs.s3.enabled"
            ]
            if key_vals:
                key = key_vals[0]
                if key.raw["Value"] in FALSE_OPTIONS:
                    yield key.inner["Value"]
            else:
                yield AWSElbV2(
                    column=attrs.start_column,
                    data=attrs.data,
                    line=get_line_by_extension(attrs.start_line, file_ext),
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
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            tfm_elb_logging_disabled_iterate_vulnerabilities(
                buckets_iterator=iter_aws_elb(model=model)
            )
        ),
        path=path,
    )


def _cfn_has_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            _has_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                ),
            )
        ),
        path=path,
    )


def _cfn_bucket_has_access_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.has_logging_disabled",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            _cfn_bucket_has_access_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
    )


def _cfn_trails_not_multiregion(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.trails_not_multiregion",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            _cfn_trails_not_multiregion_iterate_vulnerabilities(
                file_ext=file_ext,
                trails_iterator=iter_cloudtrail_trail(template=template),
            )
        ),
        path=path,
    )


def _cfn_elb_has_access_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.elb_has_access_logging_disabled",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
    )


def _cfn_elb2_has_access_logs_s3_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F200_CWE},
        description_key="src.lib_path.f200.elb2_has_access_logs_s3_disabled",
        finding=_FINDING_F200,
        iterator=get_aws_iterator(
            _cfn_elb2_has_access_logs_s3_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb2_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
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
async def cfn_trails_not_multiregion(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_trails_not_multiregion,
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


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_elb_has_access_logging_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_elb_has_access_logging_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_elb2_has_access_logs_s3_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_elb2_has_access_logs_s3_disabled,
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
            coroutines.append(
                cfn_trails_not_multiregion(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_elb_has_access_logging_disabled(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_elb2_has_access_logs_s3_disabled(
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
