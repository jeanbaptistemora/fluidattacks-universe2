# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from aws.iam.structure import (
    is_action_permissive,
    is_resource_permissive,
)
from aws.model import (
    AWSIamPolicyStatement,
)
from aws.iam.utils import (
    match_pattern,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from parse_cfn.loader import (
    load as load_cfn,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    blocking_to_snippet,
)
from zone import (
    t,
)


def _is_iam_passrole(action: str) -> bool:
    return match_pattern(action, 'iam:PassRole')


def _create_vulns(
    content: str,
    description_key: str,
    path: str,
    statements_iterator: Iterator[AWSIamPolicyStatement],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        Vulnerability(
            finding=FindingEnum.F031_AWS,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_no}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key=description_key,
                    path=path,
                ),
                snippet=blocking_to_snippet(
                    column=column_no,
                    content=content,
                    line=line_no,
                )
            )
        )
        for stmt in statements_iterator
        for column_no in [stmt.column]
        for line_no in [stmt.line]
    )


def _negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[AWSIamPolicyStatement]
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in statements_iterator:
        if stmt.data['Effect'] != 'Allow':
            continue

        if 'NotAction' in stmt.data:
            if not any(map(is_action_permissive, stmt.data['NotAction'])):
                yield stmt

        if 'NotResource' in stmt.data:
            if not any(map(is_resource_permissive, stmt.data['NotResource'])):
                yield stmt


def _permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[AWSIamPolicyStatement]
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in statements_iterator:
        if stmt.data['Effect'] == 'Allow':
            actions = stmt.data.get('Action', [])
            resources = stmt.data.get('Resource', [])

            if all((
                any(map(is_action_permissive, actions)),
                any(map(is_resource_permissive, resources)),
            )):
                yield stmt


def _open_passrole_iterate_vulnerabilities(
    statements_iterator: Iterator[AWSIamPolicyStatement]
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in statements_iterator:
        if stmt.data['Effect'] == 'Allow':
            actions = stmt.data.get('Action', [])
            resources = stmt.data.get('Resource', [])

            if all((
                any(map(_is_iam_passrole, actions)),
                any(map(is_resource_permissive, resources)),
            )):
                yield stmt


def _cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@cache_decorator()
@SHIELD
async def cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cloudconformity IAM-061
    # cfn_nag W14 IAM role should not allow Allow+NotAction on trust perms
    # cfn_nag W15 IAM role should not allow Allow+NotAction
    # cfn_nag W16 IAM policy should not allow Allow+NotAction
    # cfn_nag W17 IAM managed policy should not allow Allow+NotAction
    # cfn_nag W21 IAM role should not allow Allow+NotResource
    # cfn_nag W22 IAM policy should not allow Allow+NotResource
    # cfn_nag W23 IAM managed policy should not allow Allow+NotResource
    return await in_process(
        _cfn_negative_statement,
        content=content,
        path=path,
        template=template,
    )


def _cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@cache_decorator()
@SHIELD
async def cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cloudconformity IAM-045
    # cloudconformity IAM-049
    # cfn_nag W11 IAM role should not allow * resource on its permissions pol
    # cfn_nag W12 IAM policy should not allow * resource
    # cfn_nag W13 IAM managed policy should not allow * resource
    # cfn_nag F2 IAM role should not allow * action on its trust policy
    # cfn_nag F3 IAM role should not allow * action on its permissions policy
    # cfn_nag F4 IAM policy should not allow * action
    # cfn_nag F5 IAM managed policy should not allow * action
    return await in_process(
        _cfn_permissive_policy,
        content=content,
        path=path,
        template=template,
    )


def _cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
        path=path,
        statements_iterator=_open_passrole_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@cache_decorator()
@SHIELD
async def cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        _cfn_open_passrole,
        content=content,
        path=path,
        template=template,
    )


def _terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    # cloudconformity IAM-061
    # cfn_nag W14 IAM role should not allow Allow+NotAction on trust perms
    # cfn_nag W15 IAM role should not allow Allow+NotAction
    # cfn_nag W16 IAM policy should not allow Allow+NotAction
    # cfn_nag W17 IAM managed policy should not allow Allow+NotAction
    # cfn_nag W21 IAM role should not allow Allow+NotResource
    # cfn_nag W22 IAM policy should not allow Allow+NotResource
    # cfn_nag W23 IAM managed policy should not allow Allow+NotResource
    return await in_process(
        _terraform_negative_statement,
        content=content,
        path=path,
        model=model,
    )


def _terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
        path=path,
        statements_iterator=_open_passrole_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        _terraform_open_passrole,
        content=content,
        path=path,
        model=model,
    )


def _terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
    # cloudconformity IAM-045
    # cloudconformity IAM-049
    # cfn_nag W11 IAM role should not allow * resource on its permissions pol
    # cfn_nag W12 IAM policy should not allow * resource
    # cfn_nag W13 IAM managed policy should not allow * resource
    # cfn_nag F2 IAM role should not allow * action on its trust policy
    # cfn_nag F3 IAM role should not allow * action on its permissions policy
    # cfn_nag F4 IAM policy should not allow * action
    # cfn_nag F5 IAM managed policy should not allow * action
    return await in_process(
        _terraform_permissive_policy,
        content=content,
        path=path,
        model=model,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        template = await load_cfn(content=content, fmt=file_extension)
        coroutines.append(cfn_negative_statement(
            content=content,
            path=path,
            template=template,
        ))
        coroutines.append(cfn_open_passrole(
            content=content,
            path=path,
            template=template,
        ))
        coroutines.append(cfn_permissive_policy(
            content=content,
            path=path,
            template=template,
        ))
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(terraform_negative_statement(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_open_passrole(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_permissive_policy(
            content=content,
            path=path,
            model=model,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
