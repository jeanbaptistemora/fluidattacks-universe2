from typing import (
    Any,
    Dict,
)

MAIL_PREFERENCES: Dict[str, Dict[str, Any]] = dict(
    devsecops_agent=dict(
        email_preferences="AGENT_TOKEN",
        exclude_trial=False,
        only_fluid_staff=False,
        roles={"user_manager"},
    ),
)
