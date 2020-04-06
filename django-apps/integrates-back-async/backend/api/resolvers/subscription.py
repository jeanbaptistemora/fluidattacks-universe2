# pylint: disable=import-error

import asyncio
import sys

from backend.decorators import require_login, enforce_user_level_auth_async
from backend import util

from ariadne import convert_kwargs_to_snake_case


QUEUE = asyncio.Queue()


@convert_kwargs_to_snake_case
def resolve_subscription_mutation(obj, info, **parameters):
    """Wrap me mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@require_login
@enforce_user_level_auth_async
async def _do_post_broadcast_message(*_, message):
    """Broadcast message mutation."""
    await QUEUE.put(message)
    return dict(success=True)


async def broadcast_generator(*_):
    """Broadcast message generator."""
    while True:
        event = await QUEUE.get()
        yield event


def broadcast_resolver(event, _):
    """Broadcast message resolver."""
    return f'Broadcast message from FluidAttacks team: {event}'
