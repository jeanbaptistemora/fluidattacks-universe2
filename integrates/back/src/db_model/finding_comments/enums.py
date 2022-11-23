from enum import (
    Enum,
)


class CommentType(str, Enum):
    COMMENT: str = "COMMENT"
    CONSULT: str = "CONSULT"
    OBSERVATION: str = "OBSERVATION"
    VERIFICATION: str = "VERIFICATION"
    ZERO_RISK: str = "ZERO_RISK"
