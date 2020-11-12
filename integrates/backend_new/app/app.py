# Starlette views file

# Standard library
import os
from typing import Any, List, Sequence

# Third party libraries
from asgiref.sync import async_to_sync

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response
)
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from authlib.integrations.starlette_client import OAuth
from magic import Magic

# Local libraries
from backend.api import IntegratesAPI
from backend.api.schema import SCHEMA
from backend.dal.helpers.s3 import (
    download_file,
    list_files,
)
from backend.decorators import authenticate
from backend.services import (
    has_access_to_finding,
    has_access_to_event
)
from backend import authz as bauthz, util

import backend_new.app.utils as utils
from backend_new.app.middleware import CustomRequestMiddleware
from backend_new import settings

from __init__ import (
    FI_STARLETTE_TEST_KEY,
    FI_AWS_S3_BUCKET
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')

BUCKET_S3 = FI_AWS_S3_BUCKET
TEMPLATING_ENGINE = Jinja2Templates(directory=settings.TEMPLATES_DIR)

OAUTH = OAuth()
OAUTH.register(**settings.GOOGLE_ARGS)
OAUTH.register(**settings.AZURE_ARGS)
OAUTH.register(**settings.BITBUCKET_ARGS)


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


async def do_google_login(request: Request) -> Any:
    redirect_uri = utils.get_redirect_url(request, 'authz_google')
    google = OAUTH.create_client('google')
    return await google.authorize_redirect(request, redirect_uri)


async def do_azure_login(request: Request) -> Any:
    redirect_uri = utils.get_redirect_url(request, 'authz_azure')
    azure = OAUTH.create_client('azure')
    return await azure.authorize_redirect(request, redirect_uri)


async def do_bitbucket_login(request: Request) -> Any:
    redirect_uri = utils.get_redirect_url(request, 'authz_bitbucket')
    bitbucket = OAUTH.create_client('bitbucket')
    return await bitbucket.authorize_redirect(request, redirect_uri)


async def authz(request: Request, client: OAuth) -> RedirectResponse:
    token = await client.authorize_access_token(request)

    if 'id_token' in token:
        user = await utils.get_jwt_userinfo(client, request, token)
    else:
        user = await utils.get_bitbucket_oauth_userinfo(client, token)

    request.session['username'] = user['email']
    request.session['first_name'] = user.get('given_name', '')
    request.session['last_name'] = user.get('family_name', '')

    await utils.create_user(request.session)
    request.session['registered'] = 'True'

    return RedirectResponse(url='/new/home')


@authenticate  # type: ignore
@async_to_sync  # type: ignore
async def app(*request_args: Request) -> HTMLResponse:
    """ View for authenticated users"""
    request = utils.get_starlette_request(request_args)
    if 'username' in request.session:
        response = TEMPLATING_ENGINE.TemplateResponse(
            name='app.html',
            context={
                'request': request,
                'debug': settings.DEBUG,
                'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
                'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css',
                'delighted': f'{settings.STATIC_URL}/app/delighted.js'
            }
        )

        jwt_token = utils.create_session_token(request.session)
        utils.set_token_in_response(response, jwt_token)
    else:
        response = TEMPLATING_ENGINE.TemplateResponse(
            name='unauthorized.html',
            context={
                'request': request,
                'debug': settings.DEBUG,
            }
        )
        response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def authz_google(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.google)


async def authz_azure(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.azure)


async def authz_bitbucket(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.bitbucket)


async def enforce_group_level_role(
    request: Request,
    group: str,
    *allowed_roles: Sequence[str]
) -> Response:
    response = None
    email = request.session.get('username')
    registered = request.session.get('registered')

    if not email or not registered:
        return Response(
            '<script> '
            'var getUrl=window.location.href.split('
            '`${window.location.host}/`); '
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/"; '
            '</script>'
        )

    requester_role = await bauthz.get_group_level_role(email, group)

    if requester_role not in allowed_roles:
        response = Response('Access denied')
        response.status_code = 403

    return response


async def get_evidence(request: Request) -> Response:
    group_name = request.path_params['group_name']
    finding_id = request.path_params['finding_id']
    file_id = request.path_params['file_id']
    evidence_type = request.path_params['evidence_type']

    allowed_roles = [
        'admin',
        'analyst',
        'closer',
        'customer',
        'customeradmin',
        'executive',
        'group_manager',
        'internal_manager',
        'resourcer',
        'reviewer'
    ]
    error = await enforce_group_level_role(
        request,
        group_name,
        *allowed_roles
    )
    if error is not None:
        return error

    username = request.session['username']
    if ((evidence_type in ['drafts', 'findings', 'vulns'] and
         await has_access_to_finding(username, finding_id)) or
        (evidence_type == 'events' and
         await has_access_to_event(username, finding_id))):
        if file_id is None:
            return Response(
                'Error - Unsent image ID',
                media_type='text/html'
            )
        evidences = await list_s3_evidences(
            f'{group_name.lower()}/{finding_id}/{file_id}'
        )
        if evidences:
            for evidence in evidences:
                start = evidence.find(finding_id) + len(finding_id)
                localfile = f'/tmp{evidence[start:]}'
                localtmp = util.replace_all(
                    localfile,
                    {'.png': '.tmp', '.gif': '.tmp'}
                )
                await download_file(BUCKET_S3, evidence, localtmp)
                return retrieve_image(request, localtmp)
        else:
            return JSONResponse(
                {
                    'data': [],
                    'message': 'Access denied or evidence not found',
                    'error': True
                }
            )
    else:
        util.cloudwatch_log(
            request,
            f'Security: Attempted to retrieve evidence without permission'
        )
        return JSONResponse(
            {
                'data': [],
                'message': 'Evidence type not found',
                'error': True
            }
        )


async def list_s3_evidences(prefix: str) -> List[str]:
    return list(await list_files(BUCKET_S3, prefix))


def retrieve_image(request: Request, img_file: str) -> Response:
    if util.assert_file_mime(
            img_file,
            ['image/png', 'image/jpeg', 'image/gif']):
        with open(img_file, 'rb') as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return Response(file_obj.read(), media_type=mime_type)
    else:
        return Response(
            'Error: Invalid evidence image format',
            media_type='text/html'
        )


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/new/', login),
        Route('/new/authz_google', authz_google),
        Route('/new/authz_azure', authz_azure),
        Route('/new/authz_bitbucket', authz_bitbucket),
        Route('/new/dglogin', do_google_login),
        Route('/new/dalogin', do_azure_login),
        Route('/new/dblogin', do_bitbucket_login),
        Route('/new/api/', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/error401', error401),
        Route('/error500', error500),
        Route('/new/app', app),
        Route(
            '/new/orgs/{org_name:path}/groups/'
            '{group_name:path}/{evidence_type:path}/'
            '{finding_id:path}/{_:path}/{file_id:path}',
            get_evidence
        ),
        Route('/new/{full_path:path}', app),
        Route('/invalid_invitation', invalid_invitation),
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
