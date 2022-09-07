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
from contextlib import (
    suppress,
)
from db_model.findings.types import (
    Finding,
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
    get_finding_code_from_title,
    queue_job_new,
)
from typing import (
    List,
    Optional,
    Set,
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
    finding_id: str,
    root_nicknames: List[str],
) -> SimplePayloadMessage:
    finding_loader = info.context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    group_name: str = finding.group_name
    finding_title: str = finding.title
    _root_nicknames: Set[str] = {
        root.state.nickname
        for root in await info.context.loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot)
    }
    if not root_nicknames:
        return SimplePayloadMessage(
            success=False, message="GitRoot does not exists"
        )

    finding_code: Optional[str] = get_finding_code_from_title(finding_title)

    if finding_code is None:
        return SimplePayloadMessage(
            success=False, message="The finding cannot be found"
        )
    success = False
    with suppress(ClientError):
        roots_to_execute = _root_nicknames.intersection(root_nicknames)
        queued_job = await queue_job_new(
            dataloaders=info.context.loaders,
            finding_codes=[finding_code],
            group_name=group_name,
            roots=list(roots_to_execute),
        )
        if queued_job is not None:
            success = queued_job.success
    return SimplePayloadMessage(
        success=success,
        message="",
    )
