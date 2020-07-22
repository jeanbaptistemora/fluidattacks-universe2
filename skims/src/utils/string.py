# Standard library
from difflib import SequenceMatcher
from io import (
    BytesIO,
)

# Local libraries
from utils.aio import (
    unblock,
)


def are_similar(string_a: str, string_b: str, threshold: float = 0.85) -> bool:
    return SequenceMatcher(None, string_a, string_b).ratio() >= threshold


async def to_in_memory_file(string: str) -> BytesIO:

    def _to_in_memory_file() -> BytesIO:
        return BytesIO(string.encode())

    return await unblock(_to_in_memory_file)
