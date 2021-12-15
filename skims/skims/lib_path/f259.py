from aioextensions import (
    in_process,
)
from aws.model import (
    AWSDynamoDBTable,
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
    iter_dynamodb_table,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_dynambodb_table,
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

_FINDING_F259 = core_model.FindingEnum.F259
_FINDING_F259_CWE = _FINDING_F259.value.cwe


def cfn_has_not_point_in_time_recovery_iterate_vulnerabilities(
    file_ext: str,
    tables_iterator: Iterator[Node],
) -> Iterator[Union[AWSDynamoDBTable, Node]]:
    values = ["false", "False", False, "0", 0]
    for table in tables_iterator:
        pt_recovery = get_node_by_keys(
            table,
            ["PointInTimeRecoverySpecification", "PointInTimeRecoveryEnabled"],
        )
        if isinstance(pt_recovery, Node):
            if pt_recovery.raw in values:
                yield pt_recovery
        else:
            yield AWSDynamoDBTable(
                data=table.data,
                column=table.start_column,
                line=get_line_by_extension(table.start_line, file_ext),
            )


def tfm_db_no_point_in_time_recovery_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        recovery_attr = False
        if recovery := get_argument(
            key="point_in_time_recovery",
            body=bucket.data,
        ):
            recovery_attr = True
            if recovery_attr := get_block_attribute(
                block=recovery, key="enabled"
            ):
                if recovery_attr.val is False:
                    yield recovery_attr
        if not recovery_attr:
            yield bucket


def _cfn_has_not_point_in_time_recovery(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F259_CWE},
        description_key="src.lib_path.f259.has_not_point_in_time_recovery",
        finding=_FINDING_F259,
        iterator=get_cloud_iterator(
            cfn_has_not_point_in_time_recovery_iterate_vulnerabilities(
                file_ext=file_ext,
                tables_iterator=iter_dynamodb_table(template=template),
            )
        ),
        path=path,
    )


def _tfm_db_no_point_in_time_recovery(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F259_CWE},
        description_key="src.lib_path.f259.has_not_point_in_time_recovery",
        finding=_FINDING_F259,
        iterator=get_cloud_iterator(
            tfm_db_no_point_in_time_recovery_iterate_vulnerabilities(
                buckets_iterator=iter_aws_dynambodb_table(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_has_not_point_in_time_recovery(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_has_not_point_in_time_recovery,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_no_point_in_time_recovery(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_no_point_in_time_recovery,
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
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_has_not_point_in_time_recovery(
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
            tfm_db_no_point_in_time_recovery(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
