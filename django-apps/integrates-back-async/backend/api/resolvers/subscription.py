# pylint: disable=import-error

import asyncio
import sys
from typing import AsyncGenerator

from backend.decorators import require_login, enforce_user_level_auth_async
from backend.typing import SimplePayload as SimplePayloadType
from backend import util

from ariadne import convert_kwargs_to_snake_case


QUEUE: asyncio.Queue = asyncio.Queue()


@convert_kwargs_to_snake_case
async def resolve_subscription_mutation(obj, info, **parameters):
    """Wrap me mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


@require_login
@enforce_user_level_auth_async
async def _do_post_broadcast_message(*_, message: str) -> SimplePayloadType:
    """Broadcast message mutation."""
    await QUEUE.put(message)
    return SimplePayloadType(success=True)


async def broadcast_generator(*_) -> AsyncGenerator[str, None]:
    """Broadcast message generator."""
    while True:
        event = await QUEUE.get()
        yield event


@require_login
def broadcast_resolver(event: str, _) -> str:
    """Broadcast message resolver."""
    return f'Broadcast message from FluidAttacks team: {event}'
