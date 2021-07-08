from enum import (
    Enum,
)


class Source(Enum):
    ASM: str = "ASM"
    ESCAPE: str = "ESCAPE"
    MACHINE: str = "MACHINE"
