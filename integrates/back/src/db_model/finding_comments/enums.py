from enum import (
    Enum,
)


class CommentType(Enum):
    COMMENT: str = "COMMENT"
    VERIFICATION: str = "VERIFICATION"
    OBSERVATION: str = "OBSERVATION"
    ZERO_RISK: str = "ZERO_RISK"
    CONSULT: str = "CONSULT"
