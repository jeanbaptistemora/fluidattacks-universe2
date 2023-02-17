from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    AddDraftPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    HasRejectedDrafts,
    MachineCanNotOperate,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.utils import (
    filter_non_state_status_findings,
    has_rejected_drafts,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.availability import (
    operation_can_be_executed,
)
from newutils import (
    logs as logs_utils,
    requests as requests_utils,
)
from newutils.requests import (
    get_source_new,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@rename_kwargs({"project_name": "group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    title: str,
    **kwargs: Any,
) -> AddDraftPayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    if get_source_new(info.context) != Source.MACHINE:
        # Non rejected check
        user_drafts = await loaders.me_drafts.load(user_email)
        if has_rejected_drafts(drafts=user_drafts):
            raise HasRejectedDrafts()

    try:
        # Duplicate check
        drafts_and_findings = await loaders.group_drafts_and_findings.load(
            group_name
        )
        drafts = filter_non_state_status_findings(
            drafts_and_findings,
            {
                FindingStateStatus.APPROVED,
                FindingStateStatus.DELETED,
                FindingStateStatus.MASKED,
            },
        )
        findings = filter_non_state_status_findings(
            drafts_and_findings,
            {
                FindingStateStatus.CREATED,
                FindingStateStatus.DELETED,
                FindingStateStatus.MASKED,
                FindingStateStatus.REJECTED,
                FindingStateStatus.SUBMITTED,
            },
        )
        draft_info = findings_domain.get_draft_info(
            drafts=drafts,
            findings=findings,
            user_email=user_email,
            title=title,
            **kwargs,
        )
        if not operation_can_be_executed(info.context, draft_info.title):
            raise MachineCanNotOperate()

        draft = await findings_domain.add_draft(
            loaders,
            group_name,
            user_email,
            draft_info,
            source=requests_utils.get_source_new(info.context),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created draft in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to create draft in {group_name} group",
        )
        raise

    return AddDraftPayload(draft_id=draft.id, success=True)
