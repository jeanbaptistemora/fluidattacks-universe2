from aioextensions import (
    in_process,
)
from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
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
    iter_rds_clusters_and_instances,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_db_instance,
    iter_aws_rds_cluster,
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

_FINDING_F109 = core_model.FindingEnum.F109
_FINDING_F109_CWE = _FINDING_F109.value.cwe


def tfm_db_cluster_inside_subnet_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        subnet = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "db_subnet_group_name"
            ):
                subnet = True
        if not subnet:
            yield bucket


def tfm_rds_instance_inside_subnet_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        subnet = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "db_subnet_group_name"
            ):
                subnet = True
        if not subnet:
            yield bucket


def _cfn_rds_is_not_inside_a_db_subnet_group_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        if "DBSubnetGroupName" not in rds_res.raw:
            yield AWSRdsCluster(
                column=rds_res.start_column,
                data=rds_res.data,
                line=get_line_by_extension(rds_res.start_line, file_ext),
            )


def _tfm_db_cluster_inside_subnet(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F109_CWE},
        description_key="F109.title",
        finding=_FINDING_F109,
        iterator=get_cloud_iterator(
            tfm_db_cluster_inside_subnet_iterate_vulnerabilities(
                buckets_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


def _tfm_rds_instance_inside_subnet(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F109_CWE},
        description_key="F109.title",
        finding=_FINDING_F109,
        iterator=get_cloud_iterator(
            tfm_rds_instance_inside_subnet_iterate_vulnerabilities(
                buckets_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )


def _cfn_rds_is_not_inside_a_db_subnet_group(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F109_CWE},
        description_key=(
            "src.lib_path.f109.rds_is_not_inside_a_db_subnet_group"
        ),
        finding=_FINDING_F109,
        iterator=get_cloud_iterator(
            _cfn_rds_is_not_inside_a_db_subnet_group_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_cluster_inside_subnet(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_cluster_inside_subnet,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_rds_instance_inside_subnet(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_rds_instance_inside_subnet,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_rds_is_not_inside_a_db_subnet_group(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_rds_is_not_inside_a_db_subnet_group,
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
                cfn_rds_is_not_inside_a_db_subnet_group(
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
            tfm_db_cluster_inside_subnet(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_rds_instance_inside_subnet(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
