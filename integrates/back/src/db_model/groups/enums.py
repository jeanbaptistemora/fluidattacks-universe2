from enum import (
    Enum,
)


class GroupLanguage(str, Enum):
    EN: str = "EN"
    ES: str = "ES"


class GroupManaged(str, Enum):
    MANAGED: str = "MANAGED"
    NOT_MANAGED: str = "NOT_MANAGED"
    UNDER_REVIEW: str = "UNDER_REVIEW"
    TRIAL: str = "TRIAL"


class GroupService(str, Enum):
    BLACK: str = "BLACK"
    WHITE: str = "WHITE"


class GroupStateJustification(str, Enum):
    BUDGET: str = "BUDGET"
    DIFF_SECTST: str = "DIFF_SECTST"
    GROUP_FINALIZATION: str = "GROUP_FINALIZATION"
    GROUP_SUSPENSION: str = "GROUP_SUSPENSION"
    MIGRATION: str = "MIGRATION"
    NONE: str = "NONE"
    NO_SECTST: str = "NO_SECTST"
    NO_SYSTEM: str = "NO_SYSTEM"
    OTHER: str = "OTHER"
    RENAME: str = "RENAME"
    TRIAL_FINALIZATION: str = "TRIAL_FINALIZATION"


class GroupStateStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    DELETED: str = "DELETED"


class GroupSubscriptionType(str, Enum):
    CONTINUOUS: str = "CONTINUOUS"
    ONESHOT: str = "ONESHOT"


class GroupTier(str, Enum):
    FREE: str = "FREE"
    MACHINE: str = "MACHINE"
    ONESHOT: str = "ONESHOT"
    OTHER: str = "OTHER"
    SQUAD: str = "SQUAD"
