# Starlette templates renders

# Third party libraries
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# Local libraries
from backend_new import settings


TEMPLATING_ENGINE = Jinja2Templates(directory=settings.TEMPLATES_DIR)


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


def invalid_invitation(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='invalid_invitation.html',
        context={'request': request}
    )


def unauthorized(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='unauthorized.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
        }
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='login.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
            'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
            'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css'
        }
    )


def main_app(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='app.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
            'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
            'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css',
            'delighted': f'{settings.STATIC_URL}/app/delighted.js'
        }
    )
