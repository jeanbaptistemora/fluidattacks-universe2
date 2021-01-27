# Starlette app init file

# Third party libraries
import bugsnag
from bugsnag.asgi import BugsnagMiddleware
import newrelic.agent
import sqreen

from aioextensions import in_thread

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    RedirectResponse
)
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

# Local libraries
from backend.api import IntegratesAPI
from backend.dal import (
    session as session_dal,
)
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

from back.app.middleware import CustomRequestMiddleware
from back.app import utils
from back.app.views import (
    auth,
    charts,
    evidence,
    templates
)

from back import settings

from __init__ import (
    FI_ENVIRONMENT,
    FI_STARLETTE_SESSION_KEY
)


@authenticate_session  # type: ignore
async def app(*request_args: Request) -> HTMLResponse:
    """ View for authenticated users"""
    request = utils.get_starlette_request(request_args)
    email = request.session.get('username')
    try:
        if FI_ENVIRONMENT == 'production':
            await session_dal.check_concurrent_sessions(
                safe_encode(email),
                request.session['session_key']
            )

        if email:
            if not await org_domain.get_user_organizations(email):
                response = templates.unauthorized(request)
            else:
                response = templates.main_app(request)

                jwt_token = utils.create_session_token(request.session)
                utils.set_token_in_response(response, jwt_token)
        else:
            response = templates.unauthorized(request)
            response.delete_cookie(key=settings.JWT_COOKIE_NAME)
    except ConcurrentSession:
        response = HTMLResponse(
            '<script> '
            'localStorage.setItem("concurrentSession","1"); '
            'location.assign("/registration"); '
            '</script>'
        )
    except ExpiredToken:
        response = RedirectResponse('/')

    return response


async def logout(request: Request) -> HTMLResponse:
    """Close a user's active session"""
    await session_dal.remove_element(
        f'fi_session:{safe_encode(request.session.get("username", ""))}'
    )

    request.session.clear()

    response = RedirectResponse('/')
    response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get('url_token')
    token_exists = await session_dal.element_exists(f'fi_urltoken:{url_token}')

    if token_exists:
        token_unused = await user_domain.complete_user_register(url_token)
        if token_unused:
            response = await templates.valid_invitation(request)
        else:
            response = RedirectResponse(url='/invalid_invitation')
    else:
        await in_thread(
            bugsnag.notify, Exception('Invalid token'), severity='warning'
        )
        response = RedirectResponse(url='/invalid_invitation')

    return response


STARLETTE_APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/', templates.login),
        Route('/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/authz_azure', auth.authz_azure),
        Route('/authz_bitbucket', auth.authz_bitbucket),
        Route('/authz_google', auth.authz_google),
        Route('/confirm_access/{url_token:path}', confirm_access),
        Route('/dglogin', auth.do_google_login),
        Route('/dalogin', auth.do_azure_login),
        Route('/dblogin', auth.do_bitbucket_login),
        Route('/error401', templates.error401),
        Route('/error500', templates.error500),
        Route('/graphic', charts.graphic),
        Route('/graphics-for-group', charts.graphics_for_group),
        Route('/graphics-for-organization', charts.graphics_for_organization),
        Route('/graphics-for-portfolio', charts.graphics_for_portfolio),
        Route('/graphics-report', charts.graphics_report),
        Route('/invalid_invitation', templates.invalid_invitation),
        Route('/logout', logout),
        Route(
            '/orgs/{org_name:str}/groups/'
            '{group_name:str}/{evidence_type:str}/'
            '{finding_id:str}/{_:str}/{file_id:str}',
            evidence.get_evidence
        ),
        Mount(
            '/static',
            StaticFiles(directory=f'{settings.TEMPLATES_DIR}/static'),
            name='static'
        ),
        Route('/{full_path:path}', app)
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=FI_STARLETTE_SESSION_KEY),
        Middleware(CustomRequestMiddleware)
    ]
)

BUGSNAG_WRAP = BugsnagMiddleware(STARLETTE_APP)

sqreen.start()
NEWRELIC_WRAP = newrelic.agent.ASGIApplicationWrapper(
    BUGSNAG_WRAP,
    framework=('Starlette', '0.13.8')
)

APP = NEWRELIC_WRAP
