from db_model.enums import (
    Notification,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
)

MAIL_PREFERENCES: dict[str, dict[str, Any]] = dict(
    abandoned_trial=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    access_granted=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    add_repositories=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    add_stakeholders=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    charts_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    confirm_deletion=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    consulting_digest=dict(
        email_preferences=Notification.NEW_COMMENT,
        exclude_trial=False,
        only_fluid_staff=datetime_utils.get_now().hour > 12,
        roles=dict(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    contact_sales=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    define_treatments=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    delete_finding=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    deprecation_notice=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    devsecops_agent=dict(
        email_preferences=Notification.AGENT_TOKEN,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={"user_manager"}, org={}),
    ),
    devsecops_agent_token=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    environment_report=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    event_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    events_digest=dict(
        email_preferences=Notification.EVENT_REPORT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    file_report=dict(
        email_preferences=Notification.FILE_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={
                "customer_manager",
                "hacker",
                "resourcer",
                "user_manager",
            },
            org={},
        ),
    ),
    free_trial=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    free_trial_over=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    group_alert=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={"customer_manager", "user_manager"}, org={}),
    ),
    group_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    how_improve=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    missing_environment=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    new_comment=dict(
        email_preferences=Notification.NEW_COMMENT,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    new_draft=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    new_enrolled=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    numerator_digest=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    portfolio_report=dict(
        email_preferences=Notification.PORTFOLIO_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    remediate_finding=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    reminder=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    root_added=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_cloning_status=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_credential_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    root_deactivated=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_moved=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={"customer_manager", "user_manager"}, org={}),
    ),
    support_channels=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    treatment_report=dict(
        email_preferences=Notification.UPDATED_TREATMENT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={
                "customer_manager",
                "resourcer",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    trial_ended=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    trial_ending=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    trial_reports=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    unsubmitted_draft=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    updated_credentials_owner=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={"customer_manager", "user_manager"}),
    ),
    updated_group_info=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_policies=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    updated_root=dict(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_services=dict(
        email_preferences=Notification.SERVICE_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_treatment=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    upgrade_squad=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    user_unsubscribed=dict(
        email_preferences=Notification.UNSUBSCRIPTION_ALERT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    users_weekly_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    vulnerabilities_expiring=dict(
        email_preferences=Notification.UPDATED_TREATMENT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(
            group={
                "customer_manager",
                "resourcer",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    vulnerability_assigned=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    vulnerability_rejection=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
    vulnerability_report=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=dict(group={}, org={}),
    ),
)
