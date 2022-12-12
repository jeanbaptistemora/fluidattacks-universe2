from dataloaders import (
    Dataloaders,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessRequest,
    GroupAccessState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessRequest,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    exists,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.group_access import (
    format_invitation_state as format_group_invitation_state,
)
from newutils.organization_access import (
    format_invitation_state as format_org_invitation_state,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    loaders: Dataloaders = info.context.loaders
    request_store = sessions_domain.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        group_name = request_store["group_name"]
        if await exists(loaders, group_name, parent.email):
            group_access: GroupAccess = await loaders.group_access.load(
                GroupAccessRequest(group_name=group_name, email=parent.email)
            )
        else:
            group_access = GroupAccess(
                email=parent.email,
                group_name=group_name,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_utc_now()
                ),
            )
        group_invitation_state = format_group_invitation_state(
            invitation=group_access.invitation,
            is_registered=parent.is_registered,
        )
        return group_invitation_state.value

    if entity == "ORGANIZATION":
        org_access: OrganizationAccess = (
            await loaders.organization_access.load(
                OrganizationAccessRequest(
                    organization_id=request_store["organization_id"],
                    email=parent.email,
                )
            )
        )
        org_invitation_state = format_org_invitation_state(
            invitation=org_access.invitation,
            is_registered=parent.is_registered,
        )
        return org_invitation_state.value

    return None
