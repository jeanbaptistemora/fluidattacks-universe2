# pylint:disable=too-many-lines
from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    get_recipient_first_name,
    send_mails_async,
)
import authz
from context import (
    BASE_URL,
    FI_MAIL_CUSTOMER_EXPERIENCE,
    FI_MAIL_PRODUCTION,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date,
    datetime,
)
from db_model.groups.types import (
    Group,
    GroupMetadataToUpdate,
)
from db_model.roots.types import (
    GitRootCloning,
)
from mailer import (
    utils as mailer_utils,
)
from mailer.types import (
    TrialEngagementInfo,
)
from mailer.utils import (
    get_organization_country,
    get_organization_name,
)
from newutils import (
    analytics,
    datetime as datetime_utils,
)
from typing import (
    Any,
)


async def send_mail_free_trial_start(
    loaders: Dataloaders, email_to: str, full_name: str, group_name: str
) -> None:
    first_name = full_name.split(" ")[0]
    org_name = await get_organization_name(loaders, group_name)
    org_country = await get_organization_country(loaders, group_name)
    context = {
        "country": org_country,
        "email": email_to,
        "empty_notification_notice": True,
        "enrolled_date": datetime_utils.get_as_str(
            datetime_utils.get_now(), "%Y-%m-%d %H:%M:%S %Z"
        ),
        "enrolled_name": full_name,
        "expires_date": datetime_utils.get_as_str(
            datetime_utils.get_now_plus_delta(days=21)
        ),
        "policies_link": f"{BASE_URL}/orgs/{org_name}/policies",
        "scope_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"
        ),
        "stakeholders_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/stakeholders"
        ),
    }
    await analytics.mixpanel_track(email_to, "AutoenrollSuccess")
    await send_mails_async(
        loaders,
        email_to=[email_to],
        context=context,
        subject=(
            f"[{first_name}] Continuous Hacking just started "
            "on your applications"
        ),
        template_name="free_trial",
    )
    enrolled_email_to: list = FI_MAIL_PRODUCTION.split(",")
    enrolled_email_to.extend(FI_MAIL_CUSTOMER_EXPERIENCE.split(","))
    await send_mails_async(
        loaders,
        email_to=enrolled_email_to,
        context=context,
        subject=f"[ARM] New enrolled user [{email_to}] from [{org_country}]",
        template_name="new_enrolled",
    )


async def send_mail_free_trial_over(
    loaders: Dataloaders, email_to: list[str], group_name: str
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        subject="[ARM] your free trial ends today.",
        template_name="free_trial_over",
    )


async def send_abandoned_trial_notification(
    loaders: Dataloaders,
    email_to: str,
    first_time: bool,
) -> None:
    fname = await get_recipient_first_name(loaders, email_to)
    await send_mails_async(
        loaders,
        email_to=[email_to],
        subject=(
            f"[{fname}], start your Continuous Hacking Free Trial"
            + ("" if first_time else " (reminder)")
        ),
        template_name="abandoned_trial",
    )


async def send_add_stakeholders_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "stakeholders_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/stakeholders"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], make the most of your Free Trial: "
            "add stakeholders to your group."
        ),
        template_name="add_stakeholders",
    )


async def send_define_treatments_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], define treatments for your vulnerabilities. "
            "Make the most out of your Free Trial"
        ),
        template_name="define_treatments",
    )


async def send_add_repositories_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "scope_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/scope"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], add more repos; find more vulnerabilities!"),
        template_name="add_repositories",
    )


async def send_support_channels_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(
            f"[{fname}], Need help with Continuous Hacking? "
            "Use our support channels."
        ),
        template_name="support_channels",
    )


async def send_devsecops_agent_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "devsecops_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/devsecops"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], remediate faster with our DevSecOps Agent!"),
        template_name="devsecops_agent",
    )


async def send_trial_reports_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], download vulnerability reports."),
        template_name="trial_reports",
    )


async def send_upgrade_squad_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(
            f"[{fname}], find more severe vulnerabilities with Squad Plan!"
        ),
        template_name="upgrade_squad",
    )


async def send_trial_ending_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "expires_date": datetime_utils.get_plus_delta(
            info.start_date, days=21
        ).date(),
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], your free trial ends in 3 days."),
        template_name="trial_ending",
    )


async def send_how_improve_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(f"[{fname}], how can we improve?"),
        template_name="how_improve",
    )


async def send_trial_ended_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], your free trial has ended. "
            "Here’s what you can do next."
        ),
        template_name="trial_ended",
    )


async def send_mail_access_granted(
    loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        tags=GENERAL_TAG,
        subject=f'[Fluid Attacks] Access granted to [{context["group"]}]',
        template_name="access_granted",
        is_access_granted=True,
    )


async def send_mail_group_alert(
    loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
) -> None:
    subject = (
        f'[ARM] [{context["group"]}] group deletion failed from '
        + f'[{context["organization"]}]'
        if context["attempt"] is None
        else f'[ARM] Group [{context["group"]}] has been [{context["state"]}]'
        + f' from [{context["organization"]}]'
    )
    await send_mails_async(
        loaders,
        email_to,
        context=context,
        tags=GENERAL_TAG,
        subject=(
            f'[ARM] Group [{context["group"]}] will be deleted from '
            + f'[{context["organization"]}] soon'
            if context["attempt"]
            else subject
        ),
        template_name="group_alert",
    )


async def send_mail_group_report(
    *,
    loaders: Dataloaders,
    email_to: list[str],
    context: dict[str, Any],
    report: bool = True,
) -> None:
    await send_mails_async(
        loaders,
        email_to,
        context=context,
        tags=GENERAL_TAG,
        subject=(
            f'[ARM] {context["filetype"]}{" report" if report else ""} for '
            f'[{context["group_name"]}]'
        ),
        template_name="group_report",
    )


async def send_mail_added_root(
    *,
    loaders: Dataloaders,
    branch: str,
    environment: str,
    group_name: str,
    health_check: bool,
    root_nickname: str,
    root_url: str,
    responsible: str,
    modified_date: datetime,
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
    email_to = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="root_added",
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
            "date": str(modified_date.date()),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Root added in [{group_name}]",
        template_name="root_added",
    )


async def send_mail_updated_root(
    *,
    loaders: Dataloaders,
    email_to: list[str],
    group_name: str,
    responsible: str,
    root_nickname: str,
    new_root_content: dict[str, Any],
    old_state: dict[str, Any],
    modified_date: datetime,
) -> None:
    key_format: dict[str, str] = {
        "branch": "Long term branch",
        "environment": "Pair environment",
        "gitignore": "Exclusions",
        "url": "URL",
        "includes_health_check": "Health Check",
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
            "date": str(modified_date.date()),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Root has been changed in [{group_name}]",
        template_name="updated_root",
    )


async def send_mail_updated_root_credential(
    *,
    loaders: Dataloaders,
    email_to: list[str],
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
    loaders: Dataloaders,
    activated_by: str,
    email_to: list[str],
    group_name: str,
    last_clone_date_msg: str,
    last_root_state: str,
    other: str | None,
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
            "last_clone_date": last_clone_date_msg,
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
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    is_added: bool,
    file_name: str,
    file_description: str,
    report_date: date,
    email_to: list[str],
    uploaded_date: date | None = None,
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
    loaders: Dataloaders,
    email_to: list[str],
    group_name: str,
    last_successful_clone: GitRootCloning | None,
    root_creation_date: datetime,
    root_nickname: str,
    root_id: str,
    report_date: datetime,
    modified_by: str,
    is_failed: bool,
) -> None:
    cloning_state: str = "failed" if is_failed else "changed"
    org_name = await get_organization_name(loaders, group_name)
    cloning_time_delta = None
    days_to_clone = None
    last_clone_date_format: str = ""
    if last_successful_clone and not is_failed:
        last_clone_date = last_successful_clone.modified_date
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
        "root_creation_date": str(root_creation_date.date()),
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
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    is_added: bool,
    portfolio: str,
    report_date: date,
    email_to: list[str],
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
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    group_changes: dict[str, Any],
    report_date: datetime,
    email_to: list[str],
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
            "report_date": report_date.date(),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=(f"[ARM] Group edited: [{group_name}]"),
        template_name="updated_services",
    )


async def send_mail_devsecops_agent_token(
    *,
    loaders: Dataloaders,
    email: str,
    email_to: list[str],
    group_name: str,
    had_token: bool,
    report_date: date,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    token_status: str = "reset" if had_token else "generated"
    user_role = await authz.get_group_level_role(loaders, email, group_name)

    email_context: dict[str, Any] = {
        "scope_url": (f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"),
        "group_name": group_name,
        "report_date": report_date.strftime("on %Y-%m-%d at %H:%M:%S"),
        "responsible": email,
        "user_role": user_role.replace("_", " "),
        "had_token": had_token,
    }
    await send_mails_async(
        loaders,
        email_to,
        context=email_context,
        tags=COMMENTS_TAG,
        subject="[ARM] DevSecOps Agent token "
        + f"{token_status} in [{group_name}]",
        template_name="devsecops_agent_token",
    )


async def send_mail_stakeholder_unsubscribed(
    *,
    loaders: Dataloaders,
    email: str,
    email_to: list[str],
    group_name: str,
    report_date: date,
) -> None:
    email_context: dict[str, Any] = {
        "group_name": group_name,
        "report_date": report_date.strftime("on %Y-%m-%d"),
        "user_email": email,
    }
    await send_mails_async(
        loaders,
        email_to,
        context=email_context,
        tags=COMMENTS_TAG,
        subject=f"[ARM] Unsubscription alert in [{group_name}]",
        template_name="user_unsubscribed",
    )


async def send_mail_environment_report(
    *,
    loaders: Dataloaders,
    email_to: list[str],
    group_name: str,
    responsible: str,
    git_root: str,
    git_root_url: str,
    urls_added: list[str],
    urls_deleted: list[str],
    modified_date: datetime,
    other: str | None,
    reason: str | None,
) -> None:
    user_role = await authz.get_group_level_role(
        loaders, responsible, group_name
    )
    context = {
        "group_name": group_name,
        "responsible": responsible,
        "git_root": git_root,
        "git_root_url": git_root_url,
        "urls_added": urls_added,
        "urls_deleted": urls_deleted,
        "user_role": user_role.replace("_", " "),
        "report_date": str(modified_date.date()),
        "reason": other,
    }
    if not other:
        if reason:
            context.update({"reason": reason.replace("_", " ").capitalize()})
        else:
            context.update({"reason": ""})
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=context,
        tags=GENERAL_TAG,
        subject=f"[ARM] Environment has been modified in [{group_name}]",
        template_name="environment_report",
    )


def weeks_format(val: int | None) -> str:
    return f"{val} {'week' if val == 1 else 'weeks'}"


async def send_mail_updated_group_information(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    group: Group,
    metadata: GroupMetadataToUpdate,
    report_date: datetime,
    email_to: list[str],
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
                    "from": datetime_utils.get_as_str(
                        group.sprint_start_date, "%Y-%m-%d"
                    ),
                    "to": datetime_utils.get_as_str(
                        metadata.sprint_start_date, "%Y-%m-%d"
                    ),
                }
            }
            if group.sprint_start_date and metadata.sprint_start_date
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
            "report_date": report_date.date(),
            "user_role": user_role.replace("_", " "),
        },
        tags=GENERAL_TAG,
        subject=f"[ARM] Group information has been modified in [{group_name}]",
        template_name="updated_group_info",
    )


async def send_mail_updated_policies(
    *, loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
) -> None:
    user_role = await authz.get_user_level_role(
        loaders, context["responsible"]
    )
    context["user_role"] = user_role.replace("_", " ")
    await send_mails_async(
        loaders,
        email_to,
        context=context,
        tags=GENERAL_TAG,
        subject="[ARM] Policies have been changed in "
        + f'[{context["entity_name"]}]',
        template_name="updated_policies",
    )


async def send_mail_users_weekly_report(
    *, loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
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
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: list[str],
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        tags=GENERAL_TAG,
        subject="[ARM] Reminder",
        context=context,
        template_name="reminder",
    )


async def send_mail_numerator_report(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: list[str],
    email_cc: list[str],
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


async def send_mail_consulting_digest(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: str,
    email_cc: list[str],
) -> None:
    user_login = str(email_to).split("@", maxsplit=1)[0]
    await send_mails_async(
        loaders=loaders,
        email_to=[email_to],
        email_cc=email_cc,
        tags=GENERAL_TAG,
        subject=f"[ARM] Consulting Report [{user_login}]",
        context=context,
        template_name="consulting_digest",
    )


async def send_mail_events_digest(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: list[str],
    email_cc: list[str],
) -> None:
    user_login = str(email_to).split("@", maxsplit=1)[0]
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        email_cc=email_cc,
        tags=GENERAL_TAG,
        subject=f"[ARM] Events Report [{user_login}]",
        context=context,
        template_name="events_digest",
    )


async def send_mail_missing_environment_alert(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: list[str],
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
        template_name="missing_environment",
    )


async def send_mail_treatment_alert(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: str,
    email_cc: list[str],
) -> None:
    user_login = str(email_to).split("@", maxsplit=1)[0]
    await send_mails_async(
        loaders=loaders,
        email_to=[email_to],
        email_cc=email_cc,
        tags=GENERAL_TAG,
        subject=f"[ARM] Temporary Treatment Alert [{user_login}]",
        context=context,
        template_name="vulnerabilities_expiring",
    )
