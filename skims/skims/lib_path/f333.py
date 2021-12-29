from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
    AWSIamManagedPolicy,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
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
    iter_ec2_volumes,
    iterate_iam_policy_documents,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_launch_template,
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

_FINDING_F333 = core_model.FindingEnum.F333
_FINDING_F333_CWE = _FINDING_F333.value.cwe


def ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "instance_initiated_shutdown_behavior"
                and isinstance(elem.val, str)
                and elem.val.lower() != "terminate"
            ):
                yield elem


def ec2_has_not_termination_protection_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        protection_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "disable_api_termination"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield bucket


def _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
    file_ext: str,
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        if "Encrypted" not in ec2_res.raw:
            yield AWSEC2(
                column=ec2_res.start_column,
                data=ec2_res.data,
                line=get_line_by_extension(ec2_res.start_line, file_ext),
            )
        else:
            vol_encryption = ec2_res.inner.get("Encrypted")
            if vol_encryption.raw in FALSE_OPTIONS:
                yield vol_encryption


def _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for stmt in iam_iterator:
        effect = stmt.inner.get("Effect")
        action = stmt.inner.get("Action")
        if effect and action and effect.raw == "Allow":
            if isinstance(action.raw, list):
                for act in action.data:
                    if act.raw.startswith("ssm:"):
                        yield act
            else:
                if action.raw.startswith("ssm:"):
                    yield action


def _ec2_has_terminate_shutdown_behavior(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="lib_path.f333.ec2_allows_shutdown_command",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
                buckets_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


def _ec2_has_not_termination_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="criteria.vulns.333.description",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            ec2_has_not_termination_protection_iterate_vulnerabilities(
                buckets_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="src.lib_path.f333.ec2_has_unencrypted_volumes",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unencrypted_volumes_iterate_vulnerabilities(
                file_ext=file_ext,
                ec2_iterator=iter_ec2_volumes(template=template),
            )
        ),
        path=path,
    )


def _cfn_iam_has_full_access_to_ssm(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="src.lib_path.f333.iam_has_full_access_to_ssm",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            _cfn_iam_has_full_access_to_ssm_iterate_vulnerabilities(
                iam_iterator=iterate_iam_policy_documents(template=template),
            )
        ),
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def ec2_has_terminate_shutdown_behavior(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_has_terminate_shutdown_behavior,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
@TIMEOUT_1MIN
async def ec2_has_not_termination_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_has_not_termination_protection,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unencrypted_volumes(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unencrypted_volumes,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_iam_has_full_access_to_ssm(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_iam_has_full_access_to_ssm,
        content=content,
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
                cfn_ec2_has_unencrypted_volumes(
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
            ec2_has_terminate_shutdown_behavior(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            ec2_has_not_termination_protection(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
