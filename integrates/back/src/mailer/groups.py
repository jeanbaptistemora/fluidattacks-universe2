from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async,
)
import authz
from context import (
    BASE_URL,
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_PRODUCTION,
    FI_MAIL_REVIEWERS,
)
from datetime import (
    date,
    datetime,
)
from db_model.enums import (
    Notification,
)
from db_model.group_comments.types import (
    GroupComment,
)
from db_model.groups.types import (
    Group,
    GroupMetadataToUpdate,
)
from db_model.roots.types import (
    GitRootCloning,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from mailer.utils import (
    get_organization_name,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)


async def send_mail_free_trial_start(
    loaders: Any, email_to: List[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        tags=[],
        subject="[ARM] Congratulations! You started your 21-days free-trial",
        template_name="free_trial",
    )
    await send_mails_async(
        loaders,
        email_to=[FI_MAIL_PRODUCTION],
        context=context,
        tags=[],
        subject="[ARM] New enrolled user",
        template_name="new_enrolled",
    )


async def send_mail_free_trial_over(
    loaders: Any, email_to: List[str], group_name: str
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    context = {
        "expires_date": datetime_utils.get_now(),
        "payment_link": f"{BASE_URL}/orgs/{org_name}/billing",
    }
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        tags=[],
        subject="[ARM] Want to continue with your machine plan free trial?",
        template_name="free_trial_over",
    )


async def send_abandoned_trial_registration(
    loaders: Any,
    email_to: List[str],
    context: dict[str, Any],
    first_time: bool,
) -> None:
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        tags=[],
        subject=(
            f'[{context["registered_name"]}], '
            "start your Continuous Hacking Free Trial "
            ""
            if first_time
            else "(reminder)"
        ),
        template_name="abandoned_trial_registration",
    )


async def send_mail_access_granted(
    loaders: Any, email_to: List[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders,
        email_to,
        context,
        GENERAL_TAG,
        (
            f'[ARM] Access granted to [{context["group"]}] '
            "in ARM by Fluid Attacks"
        ),
        "access_granted",
        is_access_granted=True,
    )


async def send_mail_group_report(
    loaders: Any, email_to: List[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders,
        email_to,
        context,
        GENERAL_TAG,
        f'[ARM] {context["filetype"]} report for [{context["groupname"]}]',
        "group_report",
    )


async def send_mail_comment(
    *,
    loaders: Any,
    comment_data: GroupComment,
    user_mail: str,
    recipients: List[str],
    group_name: str = "",
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    group: Group = await loaders.group.load(group_name)
    has_machine: bool = group.state.has_machine
    has_squad: bool = group.state.has_squad

    email_context: dict[str, Any] = {
        "comment": str(comment_data.content).splitlines(),
        "comment_type": "group",
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/consulting"
        ),
        "parent": str(comment_data.parent_id),
        "group": group_name,
        "has_machine": has_machine,
        "has_squad": has_squad,
        "user_email": user_mail,
    }
    stakeholders: Tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.NEW_COMMENT
        in stakeholder.notifications_preferences.email
    ]
    reviewers = FI_MAIL_REVIEWERS.split(",")
    customer_success_recipients = FI_MAIL_CUSTOMER_SUCCESS.split(",")
    await send_mails_async(
        loaders,
        [*stakeholders_email, *customer_success_recipients, *reviewers],
        email_context,
        COMMENTS_TAG,
        f"[ARM] New comment in [{group_name}]",
        "new_comment",
    )


async def send_mail_added_root(
    *,
    loaders: Any,
    branch: str,
    email_to: List[str],
    environment: str,
    group_name: str,
    health_check: bool,
    root_nickname: str,
    root_url: str,
    responsible: str,
    modified_date: str,
    vpn_required: bool,
) -> None:
    bool_translations: dict[bool, str] = {
        True: "Yes",
        False: "No",
    }
    sla_translation: dict[bool, str] = {
        True: "Applicable",
        False: "Not applicable",
    }
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    await send_mails_async(
        loaders,
        email_to=email_to,
        context={
            "branch": branch.capitalize(),
            "environment": environment.capitalize(),
            "group": group_name,
            "root_nickname": root_nickname,
            "responsible": responsible,
            "health_check": bool_translations[health_check],
            "root_url": root_url,
            "user_role": user_role.replace("_", " "),
            "sla": sla_translation[health_check],
            "vpn_required": bool_translations[vpn_required],
            "date": str(datetime_utils.get_date_from_iso_str(modified_date)),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Root added in [{group_name}]",
        template_name="root_added",
    )


async def send_mail_updated_root(
    *,
    loaders: Any,
    email_to: List[str],
    group_name: str,
    responsible: str,
    root_nickname: str,
    new_root_content: Dict[str, Any],
    old_state: Dict[str, Any],
    modified_date: str,
) -> None:
    key_format: Dict[str, str] = {
        "branch": "Long Term Branch",
        "environment": "Pair Environment",
        "gitignore": "Exclusions",
        "url": "URL",
        "includes_health_check": "Health check",
    }
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "key_format": key_format,
            "new_root_content": new_root_content,
            "old_state": old_state,
            "root_nickname": root_nickname,
            "date": str(datetime_utils.get_date_from_iso_str(modified_date)),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Root has been changed in [{group_name}]",
        template_name="updated_root",
    )


async def send_mail_updated_root_credential(
    *,
    loaders: Any,
    email_to: List[str],
    group_name: str,
    responsible: str,
    root_nickname: str,
) -> None:
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    org_name = await get_organization_name(loaders, group_name)
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group": group_name,
            "responsible": responsible,
            "root_nickname": root_nickname,
            "user_role": user_role.replace("_", " "),
            "scope_link": (
                f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"
            ),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Root credential alert in [{group_name}]",
        template_name="root_credential_report",
    )


async def send_mail_deactivated_root(
    *,
    loaders: Any,
    activated_by: str,
    email_to: List[str],
    group_name: str,
    last_clone_date: str,
    last_root_state: str,
    other: Optional[str],
    reason: str,
    root_age: int,
    root_nickname: str,
    sast_vulns: int,
    dast_vulns: int,
    responsible: str,
) -> None:
    format_last_root_state = (
        last_root_state
        if last_root_state == "OK"
        else last_root_state.capitalize()
    )
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group": group_name,
            "reason": other
            if other
            else reason.replace("_", " ").capitalize(),
            "root_age": root_age,
            "activated_by": activated_by,
            "root_nickname": root_nickname,
            "last_root_state": format_last_root_state,
            "last_clone_date": last_clone_date,
            "sast_vulns": sast_vulns,
            "dast_vulns": dast_vulns,
            "responsible": responsible,
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=(f"[ARM] Root deactivated in [{group_name}]"),
        template_name="root_deactivated",
    )


async def send_mail_file_report(
    *,
    loaders: Any,
    group_name: str,
    responsible: str,
    is_added: bool,
    file_name: str,
    file_description: str,
    report_date: date,
    email_to: List[str],
    uploaded_date: Optional[date] = None,
) -> None:
    state_format: str = "added" if is_added else "deleted"
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    uploaded_days_to_date = (
        (datetime_utils.get_now().date() - uploaded_date).days
        if uploaded_date
        else None
    )
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "state": state_format,
            "group_name": group_name,
            "responsible": responsible,
            "file_name": file_name,
            "file_description": file_description,
            "report_date": report_date,
            "user_role": user_role.replace("_", " "),
            "uploaded_date": uploaded_date,
            "uploaded_days_to_date": uploaded_days_to_date,
        },
        tags=GENERAL_TAG,
        subject=(f"[ARM] Root file {state_format} in [{group_name}]"),
        template_name="file_report",
    )


async def send_mail_root_cloning_status(  # pylint: disable=too-many-locals
    *,
    loaders: Any,
    email_to: List[str],
    group_name: str,
    last_successful_clone: Optional[GitRootCloning],
    root_creation_date: str,
    root_nickname: str,
    root_id: str,
    report_date: datetime,
    modified_by: str,
    is_failed: bool,
) -> None:
    cloning_state: str = "failed" if is_failed else "changed"
    org_name = await get_organization_name(loaders, group_name)
    last_clone_date = None
    cloning_time_delta = None
    days_to_clone = None
    last_clone_date_format: str = ""
    if last_successful_clone and not is_failed:
        last_clone_date = datetime_utils.get_datetime_from_iso_str(
            last_successful_clone.modified_date
        )
        cloning_time_delta = report_date - last_clone_date
        days_to_clone = cloning_time_delta.days
        last_clone_date_format = last_clone_date.strftime("%Y/%m/%d")

    email_context: dict[str, Any] = {
        "is_failed": is_failed,
        "days_to_clone": days_to_clone,
        "cloning_time_delta": cloning_time_delta,
        "scope_url": (f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"),
        "group": group_name,
        "last_clone_date": last_clone_date_format,
        "root_creation_date": str(
            datetime_utils.get_date_from_iso_str(root_creation_date)
        ),
        "root_nickname": root_nickname,
        "root_id": root_id,
        "modified_by": modified_by,
        "report_date": report_date.strftime("on %Y/%m/%d at %H:%M:%S"),
    }
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            f"[ARM] Root [{root_nickname}] {cloning_state} status cloning in "
            f"[{group_name}]"
        ),
        template_name="root_cloning_status",
    )


async def send_mail_portfolio_report(
    *,
    loaders: Any,
    group_name: str,
    responsible: str,
    is_added: bool,
    portfolio: str,
    report_date: date,
    email_to: List[str],
) -> None:
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "is_added": is_added,
            "group_name": group_name,
            "responsible": responsible,
            "portfolios": portfolio,
            "report_date": report_date,
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=(f"[ARM] The portfolio has been modified in [{group_name}]"),
        template_name="portfolio_report",
    )


async def send_mail_updated_services(
    *,
    loaders: Any,
    group_name: str,
    responsible: str,
    group_changes: dict[str, Any],
    report_date: str,
    email_to: List[str],
) -> None:
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    org_name = await get_organization_name(loaders, group_name)
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "group_changes": group_changes,
            "org_name": org_name.lower(),
            "report_date": datetime_utils.get_date_from_iso_str(report_date),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=(f"[ARM] Group edited: {group_name}"),
        template_name="updated_services",
    )


async def send_mail_devsecops_agent_token(
    *,
    loaders: Any,
    group_name: str,
    user_email: str,
    report_date: date,
    email_to: List[str],
    had_token: bool,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    token_status: str = "reset" if had_token else "generated"
    user_role = await authz.get_group_level_role(
        loaders, user_email, group_name
    )

    email_context: dict[str, Any] = {
        "scope_url": (f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"),
        "group_name": group_name,
        "report_date": report_date.strftime("on %Y-%m-%d at %H:%M:%S"),
        "responsible": user_email,
        "user_role": user_role.replace("_", " "),
        "had_token": had_token,
    }
    await send_mails_async(
        loaders,
        email_to,
        email_context,
        COMMENTS_TAG,
        f"[ARM] DevSecOps Agent token {token_status} in [{group_name}]",
        "devsecops_agent_token",
    )


async def send_mail_user_unsubscribed(
    *,
    loaders: Any,
    group_name: str,
    user_email: str,
    report_date: date,
    email_to: List[str],
) -> None:
    email_context: dict[str, Any] = {
        "group_name": group_name,
        "report_date": report_date.strftime("on %Y-%m-%d at %H:%M:%S"),
        "user_email": user_email,
    }
    await send_mails_async(
        loaders,
        email_to,
        email_context,
        COMMENTS_TAG,
        f"[ARM] Unsubscription alert in [{group_name}]",
        "user_unsubscribed",
    )


async def send_mail_environment_report(
    *,
    loaders: Any,
    email_to: List[str],
    group_name: str,
    responsible: str,
    git_root: str,
    git_root_url: str,
    urls_added: List[str],
    urls_deleted: List[str],
    modified_date: str,
    other: Optional[str],
    reason: Optional[str],
) -> None:
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "git_root": git_root,
            "git_root_url": git_root_url,
            "urls_added": urls_added,
            "urls_deleted": urls_deleted,
            "user_role": user_role.replace("_", " "),
            "report_date": str(
                datetime_utils.get_date_from_iso_str(modified_date)
            ),
            "reason": other
            if other
            else reason.replace("_", " ").capitalize()
            if reason
            else "",
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Environment has been modified in [{group_name}]",
        template_name="environment_report",
    )


def weeks_format(val: Optional[int]) -> str:
    return f"{val} {'week' if val == 1 else 'weeks'}"


async def send_mail_updated_group_information(
    *,
    loaders: Any,
    group_name: str,
    responsible: str,
    group: Group,
    metadata: GroupMetadataToUpdate,
    report_date: str,
    email_to: List[str],
) -> None:
    language_metadata: str = (
        metadata.language.value if metadata.language else ""
    )
    language_format: dict[str, Any] = {"EN": "English", "ES": "Spanish"}

    group_info_modified: dict[str, Any] = {
        "Business Registration Number": {
            "from": group.business_id,
            "to": metadata.business_id,
        },
        "Business Name": {
            "from": group.business_name,
            "to": metadata.business_name,
        },
        "Description": {
            "from": group.description,
            "to": metadata.description,
        },
        "Language": {
            "from": language_format[group.language.value],
            "to": language_format[language_metadata],
        },
        "Sprint Length": {
            "from": weeks_format(group.sprint_duration),
            "to": weeks_format(metadata.sprint_duration),
        },
        **(
            {
                "Sprint Start Date": {
                    "from": group.sprint_start_date,
                    "to": metadata.sprint_start_date,
                }
            }
            if metadata.sprint_start_date
            else {}
        ),
    }

    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )

    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context={
            "group_name": group_name,
            "responsible": responsible,
            "group_changes": group_info_modified,
            "report_date": datetime_utils.get_date_from_iso_str(report_date),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Group information has been modified in [{group_name}]",
        template_name="updated_group_information",
    )


async def send_mail_updated_policies(
    *, loaders: Any, email_to: List[str], context: Dict[str, Any]
) -> None:
    user_role = await authz.get_user_level_role(
        loaders, context["responsible"]
    )
    context["user_role"] = user_role.replace("_", " ")
    await send_mails_async(
        loaders,
        email_to,
        context,
        GENERAL_TAG,
        f'[ARM] Policies have been changed in [{context["entity_name"]}]',
        "updated_policies",
    )


async def send_mail_users_weekly_report(
    *, loaders: Any, email_to: List[str], context: Dict[str, Any]
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=context,
        tags=GENERAL_TAG,
        subject="[ARM] [Week #] Users Report",
        template_name="users_weekly_report",
    )


async def send_mail_reminder(
    *,
    loaders: Any,
    context: dict[str, Any],
    email_to: List[str],
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        tags=GENERAL_TAG,
        subject="[ARM] Reminder",
        context=context,
        template_name="reminder_notification",
    )


async def send_mail_numerator_report(
    *,
    loaders: Any,
    context: dict[str, Any],
    email_to: List[str],
    email_cc: List[str],
    report_date: date,
) -> None:
    user_login = str(context["responsible"]).split("@", maxsplit=1)[0]
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        email_cc=email_cc,
        tags=GENERAL_TAG,
        subject=f"[ARM] Progress Report {user_login} [{report_date}]",
        context=context,
        template_name="numerator_digest",
    )


async def send_mail_missing_environment_alert(
    *,
    loaders: Any,
    context: Dict[str, Any],
    email_to: List[str],
) -> None:
    group_name: str = context["group"]
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        tags=GENERAL_TAG,
        subject=(
            f"[ARM] ACTION NEEDED: Your group [{group_name}] is incomplete"
        ),
        context=context,
        template_name="missing_environment_alert",
    )
