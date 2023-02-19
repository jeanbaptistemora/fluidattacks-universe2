from .payloads.types import (
    SimplePayloadMessage,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    ErrorSubmittingJob,
    MachineCouldNotBeQueued,
    MachineExecutionAlreadySubmitted,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.enums import (
    RootStatus,
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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_nicknames: list[str],
) -> SimplePayloadMessage:
    loaders: Dataloaders = info.context.loaders
    _root_nicknames: set[str] = {
        root.state.nickname
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    }

    try:
        roots_to_execute = _root_nicknames.intersection(root_nicknames)
        queued_job = await queue_job_new(
            dataloaders=loaders,
            finding_codes=list(FINDINGS.keys()),
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
