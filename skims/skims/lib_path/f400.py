from aioextensions import (
    in_process,
)
from aws.model import (
    AWSElb,
    AWSS3Bucket,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    FALSE_OPTIONS,
    get_cloud_iterator,
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
    iter_elb_load_balancers,
    iter_s3_buckets,
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

_FINDING_F400 = core_model.FindingEnum.F400
_FINDING_F400_CWE = _FINDING_F400.value.cwe


def _cfn_bucket_has_logging_conf_disabled_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]],
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        logging = bucket.inner.get("LoggingConfiguration")
        if not isinstance(logging, Node):
            yield AWSS3Bucket(
                column=bucket.start_column,
                data=bucket.data,
                line=get_line_by_extension(bucket.start_line, file_ext),
            )


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


def _cfn_bucket_has_logging_conf_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F400_CWE},
        description_key="src.lib_path.f400.bucket_has_logging_conf_disabled",
        finding=_FINDING_F400,
        iterator=get_cloud_iterator(
            _cfn_bucket_has_logging_conf_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
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
        cwe={_FINDING_F400_CWE},
        description_key="src.lib_path.f400.elb_has_access_logging_disabled",
        finding=_FINDING_F400,
        iterator=get_cloud_iterator(
            _cfn_elb_has_access_logging_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_bucket_has_logging_conf_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_bucket_has_logging_conf_disabled,
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


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_bucket_has_logging_conf_disabled(
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

    return coroutines
