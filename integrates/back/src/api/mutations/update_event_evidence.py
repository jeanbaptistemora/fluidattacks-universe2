# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_now,
)
from starlette.datastructures import (
    UploadFile,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str,
    file: UploadFile,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    evidence_id = EventEvidenceId[evidence_type]
    await events_domain.validate_evidence(evidence_id, file)

    await events_domain.update_evidence(
        loaders,
        event_id,
        evidence_id,
        file,
        get_now(),
    )
    loaders.event.clear(event_id)

    return SimplePayload(success=True)
