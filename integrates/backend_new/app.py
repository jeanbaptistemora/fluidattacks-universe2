# Third party libraries
from ariadne.asgi import GraphQL
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.responses import PlainTextResponse
from starlette.routing import Route

# Local libraries
from backend.api.schema import SCHEMA
import settings


async def app(scope, receive, send):
    response = PlainTextResponse('Hello, world!')
    await response(scope, receive, send)


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/', app),
        Route(
            endpoint=GraphQLApp(
                executor_class=AsyncioExecutor,
                graphiql=True,
                schema=GraphQL(SCHEMA, debug=settings.DEBUG),
            ),
            path='/api',
        ),
    ],
)
