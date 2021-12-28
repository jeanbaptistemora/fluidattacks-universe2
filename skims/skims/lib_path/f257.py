from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
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
    iter_ec2_ltemplates_and_instances,
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

_FINDING_F257 = core_model.FindingEnum.F257
_FINDING_F257_CWE = _FINDING_F257.value.cwe


def _cfn_ec2_has_not_termination_protection_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2 in ec2_iterator:
        ec2_res_data = ec2.inner.get("LaunchTemplateData") or ec2
        if "DisableApiTermination" not in ec2_res_data.raw:
            yield AWSEC2(
                column=ec2_res_data.start_column,
                data=ec2_res_data.data,
                line=get_line_by_extension(ec2_res_data.start_line, file_ext),
            )
        else:
            dis_api_term = ec2_res_data.inner.get("DisableApiTermination")
            if dis_api_term.raw in FALSE_OPTIONS:
                yield dis_api_term


def _cfn_ec2_has_not_termination_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F257_CWE},
        description_key="src.lib_path.f257.ec2_has_not_termination_protection",
        finding=_FINDING_F257,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_not_termination_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_ltemplates_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_not_termination_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_not_termination_protection,
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
                cfn_ec2_has_not_termination_protection(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )

    return coroutines
