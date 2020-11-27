# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=no-else-return
# pylint: disable=too-many-lines
"""Views and services for FluidIntegrates."""

# Standard library
import logging
from datetime import datetime, timedelta
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    cast
)

# Third party libraries
import bugsnag
from asgiref.sync import async_to_sync
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from jose import jwt
from magic import Magic

# Local libraries
from backend import authz, util
from backend.dal.helpers.s3 import (
    download_file,
    list_files,
)
from backend.domain import (
    analytics as analytics_domain,
    user as user_domain,
)
from backend.decorators import (
    cache_content,
    require_login,
)
from backend.services import (
    has_access_to_finding,
    has_access_to_event
)

from backend_new import settings

from __init__ import (
    FI_AWS_S3_BUCKET,
)

# Constants
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

BUCKET_S3 = FI_AWS_S3_BUCKET

LOGGER = logging.getLogger(__name__)


async def create_session_token(
    *,
    email: str,
    first_name: str,
    last_name: str,
) -> str:
    jti = util.calculate_hash_token()['jti']

    token = jwt.encode(
        dict(
            user_email=email,
            first_name=first_name,
            last_name=last_name,
            exp=(
                datetime.utcnow() +
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            ),
            sub='django_session',
            jti=jti,
        ),
        algorithm='HS512',
        key=settings.JWT_SECRET,
    )

    # Save the JTI so future requests can check for concurrency
    await util.save_token(f'fi_jwt:{jti}', token, settings.SESSION_COOKIE_AGE)

    return cast(str, token)


def set_session_cookie_in_response(
    *,
    response: HttpResponse,
    token: str,
) -> None:
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        samesite=settings.JWT_COOKIE_SAMESITE,
        value=token,
        secure=True,
        httponly=True,
        max_age=settings.SESSION_COOKIE_AGE
    )


@never_cache  # type: ignore
def index(request: HttpRequest) -> HttpResponse:
    """Login view for unauthenticated users"""
    if 'local' in request.build_absolute_uri(reverse('new')):
        parameters = {'debug': settings.DEBUG}
        return render(request, 'index.html', parameters)

    return HttpResponseRedirect('new/')


def mobile(request: HttpRequest) -> HttpResponse:
    """Small devices view"""
    parameters: Dict[str, Any] = {}
    return render(request, 'mobile.html', parameters)


@never_cache  # type: ignore
@csrf_exempt  # type: ignore
@require_http_methods(['GET'])  # type: ignore
@async_to_sync  # type: ignore
@require_login  # type: ignore
async def graphic(request: HttpRequest) -> HttpResponse:
    return await analytics_domain.handle_graphic_request(request)


@never_cache  # type: ignore
@csrf_exempt  # type: ignore
@require_http_methods(['GET'])  # type: ignore
@async_to_sync  # type: ignore
@require_login  # type: ignore
async def graphics_for_group(request: HttpRequest) -> HttpResponse:
    return await _graphics_for_entity('group', request)


@never_cache  # type: ignore
@csrf_exempt  # type: ignore
@require_http_methods(['GET'])  # type: ignore
@async_to_sync  # type: ignore
@require_login  # type: ignore
async def graphics_for_organization(request: HttpRequest) -> HttpResponse:
    return await _graphics_for_entity('organization', request)


@never_cache  # type: ignore
@csrf_exempt  # type: ignore
@require_http_methods(['GET'])  # type: ignore
@async_to_sync  # type: ignore
@require_login  # type: ignore
async def graphics_for_portfolio(request: HttpRequest) -> HttpResponse:
    return await _graphics_for_entity('portfolio', request)


async def _graphics_for_entity(
    entity: str,
    request: HttpRequest,
) -> HttpResponse:
    request_data = await util.get_jwt_content(request)

    response = await analytics_domain.handle_graphics_for_entity_request(
        entity=entity,
        request=request,
    )

    set_session_cookie_in_response(
        response=response,
        token=await create_session_token(
            email=request_data['user_email'],
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
        ),
    )

    return response


@never_cache  # type: ignore
@csrf_exempt  # type: ignore
@require_http_methods(['GET'])  # type: ignore
@async_to_sync  # type: ignore
@require_login  # type: ignore
async def graphics_report(request: HttpRequest) -> HttpResponse:
    return await analytics_domain.handle_graphics_report_request(request)


@never_cache  # type: ignore
@cache_content  # type: ignore
@csrf_exempt  # type: ignore
@async_to_sync  # type: ignore
async def get_evidence(
        request: HttpRequest,
        project: str,
        evidence_type: str,
        findingid: str,
        fileid: str) -> HttpResponse:
    allowed_roles = [
        'admin', 'analyst', 'closer',
        'customer', 'customeradmin', 'executive',
        'group_manager', 'internal_manager', 'resourcer',
        'reviewer'
    ]

    username = await util.get_jwt_content(request)
    username = username.get('user_email')

    error = await enforce_group_level_role(username, project, *allowed_roles)

    if error is not None:
        return error

    if ((evidence_type in ['drafts', 'findings', 'vulns'] and
         await has_access_to_finding(username, findingid)) or
        (evidence_type == 'events' and
         await has_access_to_event(username, findingid))):
        if fileid is None:
            bugsnag.notify(Exception('Missing evidence image ID'))

            return HttpResponse(
                'Error - Unsent image ID',
                content_type='text/html'
            )
        key_list = await list_s3_evidences(
            f'{project.lower()}/{findingid}/{fileid}'
        )
        if key_list:
            for k in key_list:
                start = k.find(findingid) + len(findingid)
                localfile = '/tmp' + k[start:]
                ext = {'.png': '.tmp', '.gif': '.tmp'}
                localtmp = util.replace_all(localfile, ext)
                await download_file(BUCKET_S3, k, localtmp)
                return retrieve_image(request, localtmp)
        else:
            return util.response(
                [], 'Access denied or evidence not found', True
            )
    else:
        util.cloudwatch_log(
            request,
            'Security: Attempted to retrieve evidence without permission'
        )
        return util.response([], 'Access denied or evidence not found', True)


async def enforce_group_level_role(
        email: str,
        group: str,
        *allowed_roles: Sequence[str]) -> HttpResponse:
    if not email:
        # The user is not even authenticated. Redirect to login
        return HttpResponse(
            '<script> '
            'var getUrl=window.location.href.split('
            '`${window.location.host}/`); '
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/"; '
            '</script>'
        )

    requester_role = await authz.get_group_level_role(email, group)
    if requester_role not in allowed_roles:
        response = HttpResponse("Access denied")
        response.status_code = 403
        return response

    return None


def retrieve_image(request: HttpRequest, img_file: str) -> HttpResponse:
    if util.assert_file_mime(
            img_file,
            ['image/png', 'image/jpeg', 'image/gif']):
        with open(img_file, 'rb') as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return HttpResponse(file_obj.read(), content_type=mime_type)
    else:
        bugsnag.notify(Exception('Invalid evidence image format'))

        return HttpResponse(
            'Error: Invalid evidence image format',
            content_type='text/html'
        )


async def list_s3_evidences(prefix: str) -> List[str]:
    """return keys that begin with prefix from the evidences folder."""
    return list(await list_files(BUCKET_S3, prefix))


@async_to_sync  # type: ignore
async def confirm_access(
    request: HttpRequest,
    urltoken: str,
) -> HttpResponse:
    redir = '/'
    token_exists = await util.token_exists(f'fi_urltoken:{urltoken}')

    if token_exists:
        token_unused = await user_domain.complete_user_register(urltoken)
        if not token_unused:
            redir = '/invalid_invitation'
    else:
        bugsnag.notify(Exception("Invalid token"), severity='warning')
        redir = '/invalid_invitation'

    return redirect(redir)
