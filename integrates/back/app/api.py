# Starlette app init file

# Standard libraries
import asyncio

# Third party libraries
import newrelic.agent
from aioextensions import in_thread
from bugsnag.asgi import BugsnagMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route

# Local libraries
from back import settings
from back.app.middleware import ApiCustomRequestMiddleware
from back.settings.queue import (
    get_task,
    init_queue,
)
from backend.api import IntegratesAPI
from backend.api.schema import SCHEMA


async def queue_daemon() -> None:
    init_queue()
    while True:
        func = await get_task()
        if asyncio.iscoroutinefunction(func):
            await func()  # type: ignore
        else:
            await in_thread(func)


def start_queue_daemon() -> None:
    asyncio.create_task(queue_daemon())


STARLETTE_APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
    ],
    middleware=[
        Middleware(ApiCustomRequestMiddleware),
    ],
    on_startup=[
        start_queue_daemon,
    ]
)

BUGSNAG_WRAP = BugsnagMiddleware(STARLETTE_APP)

NEWRELIC_WRAP = newrelic.agent.ASGIApplicationWrapper(
    BUGSNAG_WRAP,
    framework=('Starlette', '0.13.8')
)

APP = NEWRELIC_WRAP
