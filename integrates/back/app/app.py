# Starlette app init file

# Standar libraries

import asyncio
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
from backend.dal.helpers.redis import (
    redis_del_entity_attr,
)
from backend.decorators import authenticate_session
from backend.domain import (
    project as group_domain,
    organization as org_domain,
)
from backend.exceptions import (
    ConcurrentSession,
    ExpiredToken,
    SecureAccessException,
)
from backend.api.schema import SCHEMA
from backend.utils import (
    user as user_utils
)

from back.app.middleware import CustomRequestMiddleware
from back.app import utils
from back.app.views import (
    auth,
    charts,
    evidence,
    templates
)

from back import settings
from back.settings.queue import (
    get_task,
    init_queue,
)

from __init__ import (
    FI_ENVIRONMENT,
    FI_STARLETTE_SESSION_KEY
)


@authenticate_session  # type: ignore
async def app(request: Request) -> HTMLResponse:
    """ View for authenticated users"""
    email = request.session.get('username')
    try:
        if email:
            if FI_ENVIRONMENT == 'production':
                await session_dal.check_session_web_validity(request)

            if not await org_domain.get_user_organizations(email):
                response = templates.unauthorized(request)
            else:
                response = templates.main_app(request)

                jwt_token = await utils.create_session_token(request.session)
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
    except (ExpiredToken, SecureAccessException):
        response = RedirectResponse('/')

    return response


async def logout(request: Request) -> HTMLResponse:
    """Close a user's active session"""
    if 'username' in request.session:
        user_email = request.session['username']
        await session_dal.remove_session_web(user_email)
        await redis_del_entity_attr(
            entity='session',
            attr='jti',
            email=user_email
        )

    request.session.clear()

    response = RedirectResponse('/')
    response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get('url_token')
    if url_token:
        project_access = await group_domain.get_access_by_url_token(url_token)

        if project_access:
            success = await user_utils.complete_register_for_group_invitation(
                project_access
            )
            if success:
                response = await templates.valid_invitation(
                    request,
                    project_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    'used',
                    project_access=project_access
                )
        else:
            await in_thread(
                bugsnag.notify, Exception('Invalid token'), severity='warning'
            )
            response = templates.invalid_invitation(
                request,
                'Invalid or Expired'
            )
    else:
        response = templates.invalid_invitation(
            request,
            'Invalid'
        )

    return response


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
    ],
    on_startup=[start_queue_daemon]
)

BUGSNAG_WRAP = BugsnagMiddleware(STARLETTE_APP)

sqreen.start()
NEWRELIC_WRAP = newrelic.agent.ASGIApplicationWrapper(
    BUGSNAG_WRAP,
    framework=('Starlette', '0.13.8')
)

APP = NEWRELIC_WRAP
