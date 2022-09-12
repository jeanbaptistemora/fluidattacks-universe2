# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
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
    _root_nicknames: set[str] = {
        root.state.nickname
        for root in await info.context.loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    }

    try:
        roots_to_execute = _root_nicknames.intersection(root_nicknames)
        queued_job = await queue_job_new(
            dataloaders=info.context.loaders,
            finding_codes=list(FINDINGS.keys()),
            group_name=group_name,
            roots=list(roots_to_execute),
        )
        if queued_job is None or not queued_job.success:
            raise ErrorSubmittingJob()
    except ClientError as ex:
        raise ErrorSubmittingJob() from ex

    return SimplePayloadMessage(
        success=True,
        message="",
    )
