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
from batch.enums import (
    Action,
    Product,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    GitCloningStatus,
    Notification,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
    URLRootItem,
)
from db_model.users.types import (
    User,
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
    datetime as datetime_utils,
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
    Optional,
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


async def deactivate_root(  # pylint: disable=too-many-locals
    info: GraphQLResolveInfo,
    root: RootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    reason: str = kwargs["reason"]
    other: Optional[str] = kwargs.get("other") if reason == "OTHER" else None
    source = requests_utils.get_source_new(info.context)
    last_status_update = await roots_domain.get_last_status_update(
        loaders,
        root.id,
    )
    historic_state_date = datetime_utils.get_datetime_from_iso_str(
        last_status_update.modified_date
    )
    last_clone_date: str = "Never cloned"
    last_root_state: str = "Unknow"
    activated_by = last_status_update.modified_by

    if (
        isinstance(root, GitRootItem)
        and root.cloning.status != GitCloningStatus.UNKNOWN
    ):
        last_clone_date = str(
            datetime_utils.get_date_from_iso_str(root.cloning.modified_date)
        )
        last_root_state = root.cloning.status.value

    users = await group_access_domain.get_group_users(group_name, active=True)
    user_roles = await collect(
        tuple(authz.get_group_level_role(user, group_name) for user in users)
    )
    email_list = [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role in {"resourcer", "customer_manager", "user_manager"}
    ]
    root_vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.root_vulnerabilities.load(root.id)
    root_vulnerabilities_nzr = filter_non_zero_risk(
        filter_non_deleted(root_vulnerabilities)
    )
    sast_vulns = [
        vuln
        for vuln in root_vulnerabilities_nzr
        if vuln.type == VulnerabilityType.LINES
    ]
    dast_vulns = [
        vuln
        for vuln in root_vulnerabilities_nzr
        if vuln.type != VulnerabilityType.LINES
    ]

    await collect(
        tuple(
            vulns_domain.close_by_exclusion(
                vulnerability=vuln,
                modified_by=user_email,
                source=source,
            )
            for vuln in root_vulnerabilities
        ),
        workers=32,
    )
    await roots_domain.deactivate_root(
        group_name=group_name,
        other=other,
        reason=reason,
        root=root,
        user_email=user_email,
    )
    if root.state.status != "INACTIVE":
        if isinstance(root, GitRootItem):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_LINES,
                entity=group_name,
                subject=user_email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
                dependsOn=[
                    {
                        "jobId": (
                            await batch_dal.put_action(
                                action=Action.REMOVE_ROOTS,
                                entity=group_name,
                                subject=user_email,
                                additional_info=root.state.nickname,
                                product_name=Product.INTEGRATES,
                            )
                        ).batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )

        if isinstance(root, (GitRootItem, URLRootItem)):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_INPUTS,
                entity=group_name,
                subject=user_email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
            )
    await update_unreliable_indicators_by_deps(
        EntityDependency.deactivate_root,
        finding_ids=list({vuln.finding_id for vuln in root_vulnerabilities}),
        root_ids=[(root.group_name, root.id)],
        vulnerability_ids=[vuln.id for vuln in root_vulnerabilities],
    )
    root_age = (datetime_utils.get_now() - historic_state_date).days
    user: Tuple[User, ...] = await loaders.user.load_many(email_list)
    users_email = [
        user.email
        for user in user
        if Notification.ROOT_MOVED in user.notifications_preferences.email
    ]
    await groups_mail.send_mail_deactivated_root(
        activated_by=activated_by,
        email_to=users_email,
        group_name=group_name,
        last_clone_date=last_clone_date,
        last_root_state=last_root_state,
        other=other,
        reason=reason,
        root_age=root_age,
        root_nickname=root.state.nickname,
        sast_vulns=str(len(sast_vulns)),
        dast_vulns=str(len(dast_vulns)),
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
