from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from batch import (
    dal as batch_dal,
)
from custom_types import (
    SimplePayload,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
    URLRootItem,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access import (
    domain as group_access_domain,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    requests as requests_utils,
    token as token_utils,
)
from newutils.vulnerabilities import (
    filter_non_deleted,
    filter_non_zero_risk,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def deactivate_root(
    info: GraphQLResolveInfo,
    root: RootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    group_name: str = kwargs["group_name"]
    loaders = info.context.loaders
    reason: str = kwargs["reason"]
    source = requests_utils.get_source_new(info.context)

    users = await group_access_domain.get_group_users(group_name, active=True)
    user_roles = await collect(
        authz.get_group_level_role(user, group_name) for user in users
    )
    email_list = [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role
        in {"customeradmin", "resourcer", "customer_manager", "user_manager"}
    ]
    root_vulns: Tuple[Vulnerability, ...] = await loaders.root_vulns.load(
        root.id
    )
    root_vulns_nzr = filter_non_zero_risk(filter_non_deleted(root_vulns))
    sast_vulns = [
        vuln for vuln in root_vulns_nzr if vuln.type == VulnerabilityType.LINES
    ]
    dast_vulns = [
        vuln for vuln in root_vulns_nzr if vuln.type != VulnerabilityType.LINES
    ]

    await collect(
        tuple(
            vulns_domain.close_by_exclusion(
                vulnerability=vuln,
                modified_by=user_email,
                source=source,
            )
            for vuln in root_vulns
        )
    )
    await roots_domain.deactivate_root(
        group_name=group_name,
        other=None,
        reason=reason,
        root=root,
        user_email=user_email,
    )
    if root.state.status != "INACTIVE":
        if isinstance(root, GitRootItem):
            await batch_dal.put_action(
                action_name="refresh_toe_lines",
                entity=group_name,
                subject=user_email,
                additional_info=root.state.nickname,
            )
        if isinstance(root, (GitRootItem, URLRootItem)):
            await batch_dal.put_action(
                action_name="refresh_toe_inputs",
                entity=group_name,
                subject=user_email,
                additional_info=root.state.nickname,
            )
    await update_unreliable_indicators_by_deps(
        EntityDependency.deactivate_root,
        finding_ids=list({vuln.finding_id for vuln in root_vulns}),
        vulnerability_ids=[vuln.id for vuln in root_vulns],
    )
    await groups_mail.send_mail_deactivated_root(
        email_to=email_list,
        group_name=group_name,
        root_nickname=root.state.nickname,
        sast_vulns=len(sast_vulns),
        dast_vulns=len(dast_vulns),
        responsible=user_email,
    )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    root_loader: DataLoader = info.context.loaders.root
    root = await root_loader.load((kwargs["group_name"], kwargs["id"]))

    if isinstance(root, GitRootItem):
        await require_service_white(deactivate_root)(
            info, root, user_email, **kwargs
        )
    else:
        await require_service_black(deactivate_root)(
            info, root, user_email, **kwargs
        )

    return SimplePayload(success=True)
