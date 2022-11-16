# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    function,
)
import collections
from custom_exceptions import (
    InvalidAuthorization,
)
from jwcrypto.jwe import (
    InvalidJWEData,
)
from jwcrypto.jwt import (
    JWTExpired,
)
import logging
import logging.config
from sessions import (
    domain as sessions_domain,
)
from settings import (
    JWT_COOKIE_NAME,
    LOGGING,
)
from typing import (
    Any,
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_jwt_content(context: Any) -> Dict[str, str]:  # noqa: MC0001
    context_store_key = function.get_id(get_jwt_content)
    if isinstance(context, dict):
        context = context.get("request", {})
    store = get_request_store(context)

    # Within the context of one request we only need to process it once
    if context_store_key in store:
        store[context_store_key]["user_email"] = store[context_store_key][
            "user_email"
        ].lower()
        return store[context_store_key]

    try:
        cookies = context.cookies
        cookie_token = cookies.get(JWT_COOKIE_NAME)
        header_token = context.headers.get("Authorization")
        token = header_token.split()[1] if header_token else cookie_token

        if not token:
            raise InvalidAuthorization()

        content = sessions_domain.decode_token(token)
        email = content["user_email"]
        if content.get("sub") == "starlette_session":
            await sessions_domain.verify_session_token(content, email)
    except JWTExpired:
        # Session expired
        raise InvalidAuthorization() from None
    except (AttributeError, IndexError) as ex:
        LOGGER.exception(ex, extra={"extra": context})
        raise InvalidAuthorization() from None
    except InvalidJWEData:
        raise InvalidAuthorization() from None
    else:
        content["user_email"] = content["user_email"].lower()
        store[context_store_key] = content
        return content


def get_request_store(context: Any) -> collections.defaultdict:
    """Returns customized store attribute of a Django/Starlette request"""
    return context.store if hasattr(context, "store") else context.state.store
