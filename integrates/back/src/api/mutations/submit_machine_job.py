from .payloads.types import (
    SimplePayloadMessage,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    ErrorSubmittingJob,
    FindingNotFound,
    MachineCouldNotBeQueued,
    MachineExecutionAlreadySubmitted,
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_job_new,
)
from typing import (
    Optional,
)


@MUTATION.field("submitMachineJob")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    root_nicknames: list[str],
) -> SimplePayloadMessage:
    loaders: Dataloaders = info.context.loaders
    finding = await findings_domain.get_finding(loaders, finding_id)
    group_name: str = finding.group_name
    finding_title: str = finding.title
    _root_nicknames: set[str] = {
        root.state.nickname
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot)
    }
    if not root_nicknames:
        raise RootNotFound()

    finding_code: Optional[str] = get_finding_code_from_title(finding_title)
    if finding_code is None:
        raise FindingNotFound()

    try:
        roots_to_execute = _root_nicknames.intersection(root_nicknames)
        queued_job = await queue_job_new(
            dataloaders=loaders,
            finding_codes=[finding_code],
            group_name=group_name,
            roots=list(roots_to_execute),
        )
        if queued_job is None:
            raise MachineCouldNotBeQueued()
        if not queued_job.success:
            raise MachineExecutionAlreadySubmitted()
    except ClientError as ex:
        raise ErrorSubmittingJob() from ex

    return SimplePayloadMessage(
        success=True,
        message="",
    )
