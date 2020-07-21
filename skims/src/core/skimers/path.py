# Local imports
from utils.logs import (
    log_blocking,
)


async def skim(path: str) -> bool:
    log_blocking('debug', 'skim(path=%s)', path)

    return True
