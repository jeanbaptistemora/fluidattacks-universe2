from .token import (
    get_jwt_content,
)
from aioextensions import (
    in_thread,
    schedule,
)
from context import (
    FI_ENVIRONMENT,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)

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
    schedule(in_thread(LOGGER_TRANSACTIONAL.info, ":".join(info)))
