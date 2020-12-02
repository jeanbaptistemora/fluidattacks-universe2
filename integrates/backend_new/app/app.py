# Starlette app init file

# Standard library
import os

# Third party libraries
import bugsnag
import newrelic.agent

from aioextensions import in_thread
from asgiref.sync import async_to_sync

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
    Response
)
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

# Local libraries
from backend import util
from backend.api import IntegratesAPI
from backend.decorators import authenticate_session
from backend.domain import (
    organization as org_domain,
    user as user_domain
)
from backend.exceptions import (
    ConcurrentSession,
    ExpiredToken
)
from backend.api.schema import SCHEMA
from backend.utils.encodings import safe_encode

from backend_new.app.middleware import CustomRequestMiddleware
from backend_new.app import utils, views
from backend_new import settings

from __init__ import (
    FI_ENVIRONMENT,
    FI_STARLETTE_TEST_KEY
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')


@authenticate_session  # type: ignore
@async_to_sync  # type: ignore
async def app(*request_args: Request) -> HTMLResponse:
    """ View for authenticated users"""
    request = utils.get_starlette_request(request_args)
    email = request.session.get('username')
    try:
        if FI_ENVIRONMENT == 'production':
            await util.check_concurrent_sessions(
                safe_encode(email),
                request.session['session_key']
            )

        if email:
            if not await org_domain.get_user_organizations(email):
                response = views.unauthorized(request)
            else:
                response = views.main_app(request)

                jwt_token = utils.create_session_token(request.session)
                utils.set_token_in_response(response, jwt_token)
        else:
            response = views.unauthorized(request)
            response.delete_cookie(key=settings.JWT_COOKIE_NAME)
    except ConcurrentSession:
        response = Response(
            '<script> '
            'localStorage.setItem("concurrentSession","1"); '
            'location.assign("/new/registration"); '
            '</script>'
        )
    except ExpiredToken:
        response = RedirectResponse('/new')

    return response


def logout(request: Request) -> HTMLResponse:
    """Close a user's active session"""
    request.session.clear()

    response = RedirectResponse('/new')
    response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get('url_token')
    redir = '/new'
    token_exists = await util.token_exists(f'fi_urltoken:{url_token}')

    if token_exists:
        token_unused = await user_domain.complete_user_register(url_token)
        if not token_unused:
            redir = '/invalid_invitation'
    else:
        await in_thread(bugsnag.notify, Exception('Invalid token'), 'warning')
        redir = '/invalid_invitation'

    return RedirectResponse(url=redir)


STARLETTE_APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/error401', views.error401),
        Route('/error500', views.error500),
        Route('/graphic', views.graphic),
        Route('/graphics-for-group', views.graphics_for_group),
        Route('/graphics-for-organization', views.graphics_for_organization),
        Route('/graphics-for-portfolio', views.graphics_for_portfolio),
        Route('/graphics-report', views.graphics_report),
        Route('/invalid_invitation', views.invalid_invitation),
        Route('/new/', views.login),
        Route('/new/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/new/authz_google', views.authz_google),
        Route('/new/authz_azure', views.authz_azure),
        Route('/new/authz_bitbucket', views.authz_bitbucket),
        Route('/new/confirm_access/{url_token:path}', confirm_access),
        Route('/new/dglogin', views.do_google_login),
        Route('/new/dalogin', views.do_azure_login),
        Route('/new/dblogin', views.do_bitbucket_login),
        Route(
            '/new/orgs/{org_name:str}/groups/'
            '{group_name:str}/{evidence_type:str}/'
            '{finding_id:str}/{_:str}/{file_id:str}',
            views.get_evidence
        ),
        Route('/logout', logout),
        Route('/new/{full_path:path}', app),
        Route('/', app),
        Mount(
            '/static',
            StaticFiles(directory=f'{settings.TEMPLATES_DIR}/static'),
            name='static'
        )
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=FI_STARLETTE_TEST_KEY),
        Middleware(CustomRequestMiddleware)
    ]
)

newrelic.agent.initialize(settings.NEW_RELIC_CONF_FILE)
APP = newrelic.agent.ASGIApplicationWrapper(
    STARLETTE_APP,
    framework=('Starlette', '0.13.8')
)
