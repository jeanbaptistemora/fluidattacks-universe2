# Starlette app init file

# Standard library
import os

# Third party libraries
from asgiref.sync import async_to_sync

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

# Local libraries
from backend.api import IntegratesAPI
from backend.decorators import authenticate_session
from backend.domain import organization as org_domain
from backend.api.schema import SCHEMA

from backend_new.app.middleware import CustomRequestMiddleware
from backend_new.app import utils, views
from backend_new import settings

from __init__ import (
    FI_STARLETTE_TEST_KEY
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')


@authenticate_session  # type: ignore
@async_to_sync  # type: ignore
async def app(*request_args: Request) -> HTMLResponse:
    """ View for authenticated users"""
    request = utils.get_starlette_request(request_args)
    email = request.session.get('username')

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

    return response


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/error401', views.error401),
        Route('/error500', views.error500),
        Route('/invalid_invitation', views.invalid_invitation),
        Route('/new/', views.login),
        Route('/new/authz_google', views.authz_google),
        Route('/new/authz_azure', views.authz_azure),
        Route('/new/authz_bitbucket', views.authz_bitbucket),
        Route('/new/dglogin', views.do_google_login),
        Route('/new/dalogin', views.do_azure_login),
        Route('/new/dblogin', views.do_bitbucket_login),
        Route('/new/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/new/confirm_access/{url_token:path}', views.confirm_access),
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
