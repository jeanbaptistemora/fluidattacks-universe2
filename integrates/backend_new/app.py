# Third party libraries
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.responses import JSONResponse
from starlette.routing import Route

# Local libraries
import backend_new.settings as settings


async def app(request):
    return JSONResponse({'hello': 'world'})


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/', app),
    ],
)
