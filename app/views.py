# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=no-else-return
# pylint: disable=too-many-lines
"""Views and services for FluidIntegrates."""

# Standard library
import os
from datetime import datetime, timedelta
from typing import (
    List,
    Dict,
    Sequence,
    Any,
    cast
)

# Third party libraries
import boto3
import bugsnag
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from jose import jwt
from magic import Magic

# Local libraries
from backend import authz, util
from backend.domain import (
    analytics as analytics_domain,
)
from backend.decorators import (
    authenticate,
    cache_content,
    require_login,
)
from backend.exceptions import ConcurrentSession
from backend.services import (
    has_access_to_finding,
    has_access_to_event
)
from __init__ import (
    FI_AWS_S3_ACCESS_KEY,
    FI_AWS_S3_SECRET_KEY,
    FI_AWS_S3_BUCKET,
    FI_ENVIRONMENT
)

# Constants
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

CLIENT_S3 = boto3.client(
    's3',
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
)

BUCKET_S3 = FI_AWS_S3_BUCKET


def enforce_user_level_role(
        request: HttpRequest,
        *allowed_roles: Sequence[str]) -> HttpResponse:
    # Verify role if the user is logged in
    email = request.session.get('username')
    registered = request.session.get('registered')

    if not email or not registered:
        # The user is not even authenticated. Redirect to login
        return HttpResponse(
            '<script> '
            'var getUrl=window.location.href.split('
            '`${window.location.host}/integrates`); '
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/integrates/index"; '
            '</script>'
        )

    requester_role = authz.get_user_level_role(email)
    if requester_role not in allowed_roles:
        response = HttpResponse("Access denied")
        response.status_code = 403
        return response

    return None


def enforce_group_level_role(
        request: HttpRequest,
        group: str,
        *allowed_roles: Sequence[str]) -> HttpResponse:
    # Verify role if the user is logged in
    email = request.session.get('username')
    registered = request.session.get('registered')

    if not email or not registered:
        # The user is not even authenticated. Redirect to login
        return HttpResponse(
            '<script> '
            'var getUrl=window.location.href.split('
            '`${window.location.host}/integrates`); '
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/integrates/index"; '
            '</script>'
        )

    requester_role = authz.get_group_level_role(email, group)
    if requester_role not in allowed_roles:
        response = HttpResponse("Access denied")
        response.status_code = 403
        return response

    return None


def create_session_token(
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
    util.save_token(f'fi_jwt:{jti}', token, settings.SESSION_COOKIE_AGE)

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
    parameters = {'debug': settings.DEBUG}
    return render(request, 'index.html', parameters)


def error500(request: HttpRequest) -> HttpResponse:
    """Internal server error view"""
    parameters: Dict[str, Any] = {}
    return render(request, 'HTTP500.html', parameters)


def error401(request: HttpRequest, _: Any) -> HttpResponse:
    """Unauthorized error view"""
    parameters: Dict[str, Any] = {}
    return render(request, 'HTTP401.html', parameters)


def mobile(request: HttpRequest) -> HttpResponse:
    """Small devices view"""
    parameters: Dict[str, Any] = {}
    return render(request, 'mobile.html', parameters)


@csrf_exempt  # type: ignore
@cache_control(private=True, max_age=3600)  # type: ignore
@authenticate  # type: ignore
def app(request: HttpRequest) -> HttpResponse:
    """App view for authenticated users."""
    try:
        if FI_ENVIRONMENT == 'production':
            util.check_concurrent_sessions(
                request.session['username'],
                request.session.session_key,
            )

        response = render(request, 'app.html', {
            'debug': settings.DEBUG,
            'username': request.session['username']
        })

        set_session_cookie_in_response(
            response=response,
            token=create_session_token(
                email=request.session['username'],
                first_name=request.session['first_name'],
                last_name=request.session['last_name'],
            ),
        )
    except KeyError as ex:
        bugsnag.notify(ex)
        return redirect('/integrates/error500')
    except ConcurrentSession:
        return HttpResponse(
            '<script> '
            'localStorage.setItem("concurrentSession","1"); '
            'location.assign("/integrates/registration"); '
            '</script>'
        )
    return response


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


async def _graphics_for_entity(
    entity: str,
    request: HttpRequest,
) -> HttpResponse:
    request_data = util.get_jwt_content(request)

    response = await analytics_domain.handle_graphics_for_entity_request(
        entity=entity,
        request=request,
    )

    set_session_cookie_in_response(
        response=response,
        token=create_session_token(
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


@csrf_exempt  # type: ignore
@authenticate  # type: ignore
def logout(request: HttpRequest) -> HttpResponse:
    """Close a user's active session"""
    try:
        jwt_cookie = request.COOKIES.get(settings.JWT_COOKIE_NAME)
        if jwt_cookie:
            cookie_content = jwt.decode(
                token=jwt_cookie,
                key=settings.JWT_SECRET,
                algorithms='HS512'
            )
            jti = cookie_content.get('jti')
            if jti:
                util.remove_token(f'fi_jwt:{jti}')

        request.session.flush()
    except KeyError as ex:
        bugsnag.notify(ex)

    response = redirect('/integrates/index')
    response.delete_cookie(settings.JWT_COOKIE_NAME)
    return response


@cache_content  # type: ignore
@cache_control(private=True, max_age=31536000)  # type: ignore
@csrf_exempt  # type: ignore
def get_evidence(
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

    error = enforce_group_level_role(request, project, *allowed_roles)

    if error is not None:
        return error

    username = request.session['username']
    if ((evidence_type in ['drafts', 'findings'] and
         has_access_to_finding(username, findingid)) or
        (evidence_type == 'events' and
         has_access_to_event(username, findingid))):
        if fileid is None:
            bugsnag.notify(Exception('Missing evidence image ID'))

            return HttpResponse(
                'Error - Unsent image ID',
                content_type='text/html'
            )
        key_list = list_s3_evidences(f'{project.lower()}/{findingid}/{fileid}')
        if key_list:
            for k in key_list:
                start = k.find(findingid) + len(findingid)
                localfile = '/tmp' + k[start:]
                ext = {'.png': '.tmp', '.gif': '.tmp'}
                localtmp = util.replace_all(localfile, ext)
                CLIENT_S3.download_file(BUCKET_S3, k, localtmp)
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


def list_s3_evidences(prefix: str) -> List[str]:
    """return keys that begin with prefix from the evidences folder."""
    return list(util.iterate_s3_keys(CLIENT_S3, BUCKET_S3, prefix))
