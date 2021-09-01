# Submit
# None


from aioextensions import (
    schedule,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    delete_kwargs,
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
from mailer import (
    findings as findings_mail,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@delete_kwargs({"group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, finding_id: str
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    analyst_email = user_info["user_email"]
    success = await findings_domain.submit_draft(
        info.context, finding_id, analyst_email
    )

    if success:
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon("submit_draft", finding_id=finding_id)
        finding_loader = info.context.loaders.finding
        finding = await finding_loader.load(finding_id)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Submitted draft {finding_id} successfully",
        )
        schedule(
            findings_mail.send_mail_new_draft(
                info.context.loaders,
                finding_id,
                finding["title"],
                str(get_key_or_fallback(finding, fallback="")),
                analyst_email,
            )
        )
    return SimplePayload(success=success)
