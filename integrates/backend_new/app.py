# Third party libraries
from ariadne.asgi import GraphQL

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Local libraries
from backend.api.schema import SCHEMA

from backend_new import settings

TEMPLATES_DIR = 'backend_new/templates'
TEMPLATING_ENGINE = Jinja2Templates(directory=TEMPLATES_DIR)


def error500(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='HTTP500.html',
        context={'request': request}
    )


def error401(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='HTTP401.html',
        context={'request': request}
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='login.html',
        context={'request': request, 'debug': settings.DEBUG}
    )


async def app(request: Request) -> JSONResponse:
    return JSONResponse({'hello': 'world'})


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/new/', app),
        Route('/new/api/', GraphQL(SCHEMA, debug=settings.DEBUG)),
        Route('/new/login/', login),
        Route('/error401', error401),
        Route('/error500', error500),
        Mount(
            '/static',
            StaticFiles(directory=f'{TEMPLATES_DIR}/static'),
            name='static'
        )
    ],
)
