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
from db_model.groups.types import (
    Group,
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
from organizations.utils import (
    get_organization,
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
    event = await events_domain.get_event(loaders, event_id)
    group: Group = await loaders.group.load(event.group_name)
    organization = await get_organization(loaders, group.organization_id)
    await events_domain.validate_evidence(
        group_name=group.name.lower(),
        organization_name=organization.name.lower(),
        evidence_id=evidence_id,
        file=file,
    )

    await events_domain.update_evidence(
        loaders=loaders,
        event_id=event_id,
        evidence_id=evidence_id,
        file=file,
        update_date=get_now(),
    )
    loaders.event.clear(event_id)

    return SimplePayload(success=True)
