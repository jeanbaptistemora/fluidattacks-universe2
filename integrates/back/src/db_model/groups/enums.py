from enum import (
    Enum,
)


class GroupLanguage(str, Enum):
    EN: str = "EN"
    ES: str = "ES"


class GroupService(str, Enum):
    BLACK: str = "BLACK"
    WHITE: str = "WHITE"


class GroupStateRemovalJustification(str, Enum):
    DIFF_SECTST: str = "DIFF_SECTST"
    MIGRATION: str = "MIGRATION"
    NO_SECTST: str = "NO_SECTST"
    NO_SYSTEM: str = "NO_SYSTEM"
    OTHER: str = "OTHER"


class GroupStateStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    DELETED: str = "DELETED"


class GroupStateUpdationJustification(str, Enum):
    BUDGET: str = "BUDGET"
    GROUP_FINALIZATION: str = "GROUP_FINALIZATION"
    GROUP_SUSPENSION: str = "GROUP_SUSPENSION"
    NONE: str = "NONE"
    OTHER: str = "OTHER"


class GroupSubscriptionType(str, Enum):
    CONTINUOUS: str = "CONTINUOUS"
    ONESHOT: str = "ONESHOT"


class GroupTier(str, Enum):
    FREE: str = "FREE"
    MACHINE: str = "MACHINE"
    SQUAD: str = "SQUAD"
    ONESHOT: str = "ONESHOT"
    OTHER: str = "OTHER"
