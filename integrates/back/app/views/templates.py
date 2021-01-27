# Starlette templates renders

# Standard library
import json
import traceback
from typing import (
    Any,
    cast,
    Dict,
)

# Third party libraries
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# Local libraries
from backend.dal import (
    session as session_dal,
)
from backend.typing import GraphicParameters

from back import settings


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


async def valid_invitation(request: Request) -> HTMLResponse:
    url_token = request.path_params['url_token']
    info = cast(
        Dict[str, Any],
        await session_dal.get_redis_element(f'fi_urltoken:{url_token}')
    )
    group_name = info['group']
    return TEMPLATING_ENGINE.TemplateResponse(
        name='valid_invitation.html',
        context={
            'group_name': group_name,
            'request': request,
        }
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
        }
    )


def graphic_error(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='graphic-error.html',
        context=dict(
            request=request,
            debug=settings.DEBUG,
            traceback=traceback.format_exc()
        )
    )


def graphics_for_entity_view(request: Request, entity: str) -> HTMLResponse:
    entity_title = entity.title()
    return TEMPLATING_ENGINE.TemplateResponse(
        name='graphics-for-entity.html',
        context=dict(
            request=request,
            debug=settings.DEBUG,
            entity=entity_title,
            js=(
                f'{settings.STATIC_URL}/dashboard/'
                f'graphicsFor{entity_title}-bundle.min.js'
            ),
            css=(
                f'{settings.STATIC_URL}/dashboard/'
                f'graphicsFor{entity_title}-style.min.css'
            )
        )
    )


def graphic_view(
    request: Request,
    document: object,
    params: GraphicParameters
) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='graphic.html',
        context=dict(
            request=request,
            args=dict(
                data=json.dumps(document),
                height=params.height,
                width=params.width,
            ),
            generator_src=(
                f'graphics/'
                f'generators/'
                f'{params.generator_type}/'
                f'{params.generator_name}.js'
            ),
            c3js=f'{settings.STATIC_URL}/external/C3/c3-0.7.18/c3.js',
            c3css=(
                f'{settings.STATIC_URL}/external/C3/c3-0.7.18/c3.css'
            )
        )
    )
