import logging
import logging.config

from aioextensions import (
    in_thread,
    schedule,
)
from starlette.requests import Request

from __init__ import FI_ENVIRONMENT
from settings import (
    LOGGING,
    NOEXTRA,
)

from .token import get_jwt_content


logging.config.dictConfig(LOGGING)

# Constants
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


def cloudwatch_log(request: Request, msg: str) -> None:
    schedule(cloudwatch_log_async(request, msg))


async def cloudwatch_log_async(request: Request, msg: str) -> None:
    user_data = await get_jwt_content(request)
    info = [str(user_data["user_email"])]
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    schedule(in_thread(LOGGER_TRANSACTIONAL.info, ":".join(info), **NOEXTRA))
