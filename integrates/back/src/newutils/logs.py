# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
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
    try:
        user_data = await get_jwt_content(request)
    except (ExpiredToken, InvalidAuthorization):
        user_data = {"user_email": "unauthenticated"}
    info = [str(user_data["user_email"])]
    info.append(FI_ENVIRONMENT)
    info.append(msg)
    schedule(in_thread(LOGGER_TRANSACTIONAL.info, ":".join(info)))
