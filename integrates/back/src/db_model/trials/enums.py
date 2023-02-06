from enum import (
    Enum,
)


class TrialStatus(str, Enum):
    EXTENDED: str = "EXTENDED"
    EXTENDED_ENDED: str = "EXTENDED_ENDED"
    TRIAL: str = "TRIAL"
    TRIAL_ENDED: str = "TRIAL_ENDED"
