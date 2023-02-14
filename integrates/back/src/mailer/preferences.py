from db_model.enums import (
    Notification,
)
from typing import (
    Any,
    Dict,
)

MAIL_PREFERENCES: Dict[str, Dict[str, Any]] = dict(
    devsecops_agent=dict(
        email_preferences=Notification.AGENT_TOKEN,
        exclude_trial=False,
        only_fluid_staff=False,
        roles={"user_manager"},
    ),
    group_alert=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles={"customer_manager", "user_manager"},
    ),
    update_group_info=dict(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles={"resourcer", "customer_manager", "user_manager"},
    ),
)
