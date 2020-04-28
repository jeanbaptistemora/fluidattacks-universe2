# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=no-else-return
# pylint: disable=too-many-lines
"""Views and services for FluidIntegrates."""

import os
import sys
from datetime import datetime, timedelta

import boto3
import rollbar
import yaml
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from jose import jwt
from magic import Magic
from openpyxl import load_workbook, Workbook

from backend import util
from backend.domain import (
    finding as finding_domain, project as project_domain, user as user_domain)
from backend.domain.vulnerability import get_vulnerabilities_by_type
from backend.decorators import authenticate, cache_content
from backend.dal import (
    finding as finding_dal, user as user_dal
)
from backend.services import (
    has_access_to_finding, has_access_to_event
)

from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
)

from app.documentator.all_vulns import generate_all_vulns_xlsx

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
                         aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))

BUCKET_S3 = FI_AWS_S3_BUCKET
BASE_URL = 'https://fluidattacks.com/integrates'


def enforce_user_level_role(request, *allowed_roles):
    # Verify role if the user is logged in
    email = request.session.get('username')
    registered = request.session.get('registered')

    if not email or not registered:
        # The user is not even authenticated. Redirect to login
        return HttpResponse("""
            <script>
                var getUrl=window.location.hash.substr(1);
                localStorage.setItem("url_inicio",getUrl);
                location = "/integrates/index";
            </script>
            """)

    requester_role = user_domain.get_user_level_role(email)
    if requester_role not in allowed_roles:
        response = HttpResponse("Access Denied")
        response.status_code = 403
        return response

    return None


def enforce_group_level_role(request, group, *allowed_roles):
    # Verify role if the user is logged in
    email = request.session.get('username')
    registered = request.session.get('registered')

    if not email or not registered:
        # The user is not even authenticated. Redirect to login
        return HttpResponse("""
            <script>
                var getUrl=window.location.hash.substr(1);
                localStorage.setItem("url_inicio",getUrl);
                location = "/integrates/index";
            </script>
            """)

    requester_role = user_domain.get_group_level_role(email, group)
    if requester_role not in allowed_roles:
        response = HttpResponse("Access Denied")
        response.status_code = 403
        return response

    return None


@never_cache
def index(request):
    """Login view for unauthenticated users"""
    parameters = {'debug': settings.DEBUG}
    return render(request, 'index.html', parameters)


def error500(request):
    """Internal server error view"""
    parameters = {}
    return render(request, 'HTTP500.html', parameters)


def error401(request, _):
    """Unauthorized error view"""
    parameters = {}
    return render(request, 'HTTP401.html', parameters)


@csrf_exempt
@cache_control(private=True, max_age=3600)
@authenticate
def app(request):
    """App view for authenticated users."""
    try:
        parameters = {
            'debug': settings.DEBUG,
            'username': request.session['username']
        }
        response = render(request, 'app.html', parameters)
        token = jwt.encode(
            {
                'user_email': request.session['username'],
                'company': request.session['company'],
                'first_name': request.session['first_name'],
                'last_name': request.session['last_name'],
                'exp': datetime.utcnow() +
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        response.set_cookie(
            key=settings.JWT_COOKIE_NAME,
            value=token,
            secure=True,
            # Temporary while ariadne migration is finished
            httponly=not settings.DEBUG,
            max_age=settings.SESSION_COOKIE_AGE
        )
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return redirect('/integrates/error500')
    return response


@csrf_exempt
@authenticate
def logout(request):
    """Close a user's active session"""

    HttpResponse("<script>Intercom('shutdown');</script>")
    try:
        request.session.flush()
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)

    response = redirect("/integrates/index")
    response.delete_cookie(settings.JWT_COOKIE_NAME)
    return response


@cache_content
@never_cache
@csrf_exempt
def get_evidence(request, project, evidence_type, findingid, fileid):
    allowed_roles = ['analyst', 'customer', 'customeradmin', 'admin']

    error = enforce_group_level_role(request, project, *allowed_roles)

    if error is not None:
        return error

    username = request.session['username']
    if (evidence_type in ['drafts', 'findings']
        and has_access_to_finding(username, findingid)) \
            or (evidence_type == 'events'
                and has_access_to_event(username, findingid)):
        if fileid is None:
            rollbar.report_message('Error: Missing evidence image ID',
                                   'error', request)
            return HttpResponse('Error - Unsent image ID',
                                content_type='text/html')
        key_list = key_existing_list(f'{project.lower()}/{findingid}/{fileid}')
        if key_list:
            for k in key_list:
                start = k.find(findingid) + len(findingid)
                localfile = '/tmp' + k[start:]
                ext = {'.png': '.tmp', '.gif': '.tmp'}
                localtmp = util.replace_all(localfile, ext)
                CLIENT_S3.download_file(BUCKET_S3, k, localtmp)
                return retrieve_image(request, localtmp)
        else:
            return util.response([], 'Access denied or evidence not found', True)
    else:
        util.cloudwatch_log(
            request,
            'Security: Attempted to retrieve evidence without permission')
        return util.response([], 'Access denied or evidence not found', True)


def retrieve_image(request, img_file):
    if util.assert_file_mime(img_file, ['image/png', 'image/jpeg',
                                        'image/gif']):
        with open(img_file, 'rb') as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return HttpResponse(file_obj.read(), content_type=mime_type)
    else:
        rollbar.report_message('Error: Invalid evidence image format',
                               'error', request)
        return HttpResponse('Error: Invalid evidence image format',
                            content_type='text/html')


def key_existing_list(key):
    """return the key's list if it exist, else list empty"""
    return util.list_s3_objects(CLIENT_S3, BUCKET_S3, key)


@cache_content
@never_cache
@csrf_exempt
@authenticate
@require_http_methods(['GET'])
def download_vulnerabilities(request, findingid):
    """Download a file with all the vulnerabilities."""
    allowed_roles = ['analyst', 'admin']

    if not has_access_to_finding(request.session['username'], findingid):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to retrieve vulnerabilities without permission')
        return util.response([], 'Access denied', True)
    else:
        group = finding_dal.get_finding(findingid).get('project_name', '')

        error = enforce_group_level_role(request, group, *allowed_roles)
        if error is not None:
            return error

        finding = get_vulnerabilities_by_type(findingid)
        data_yml = {}
        vuln_types = {'ports': dict, 'lines': dict, 'inputs': dict}
        if finding:
            for vuln_key, cast_fuction in list(vuln_types.items()):
                if finding.get(vuln_key):
                    data_yml[vuln_key] = list(map(cast_fuction, list(finding.get(vuln_key))))
                else:
                    # This finding does not have this type of vulnerabilities
                    pass
        else:
            # This finding does not have new vulnerabilities
            pass
        project = finding_domain.get_finding(findingid)['projectName']
        file_name = '/tmp/{project}-{finding_id}.yaml'.format(
            finding_id=findingid, project=project)
        stream = open(file_name, 'w')
        yaml.safe_dump(data_yml, stream, default_flow_style=False)
        try:
            with open(file_name, 'rb') as file_obj:
                response = HttpResponse(file_obj.read(), content_type='text/x-yaml')
                response['Content-Disposition'] = \
                    'attachment; filename="{project}-{finding_id}.yaml"'.format(
                        finding_id=findingid, project=project)
                return response
        except IOError:
            rollbar.report_message('Error: Invalid vulnerabilities file format', 'error', request)
            return util.response([], 'Invalid vulnerabilities file format', True)


@never_cache
@require_http_methods(["GET"])
# pylint: disable=too-many-locals
def generate_complete_report(request):
    user_data = util.get_jwt_content(request)
    projects = user_domain.get_projects(user_data['user_email'])
    book = load_workbook('/usr/src/app/app/techdoc/templates/COMPLETE.xlsx')
    sheet = book.active

    project_col = 1
    finding_col = 2
    vuln_where_col = 3
    vuln_specific_col = 4
    treatment_col = 5
    treatment_mgr_col = 6
    row_offset = 2

    row_index = row_offset
    for project in projects:
        findings = project_domain.get_released_findings(
            project, 'finding_id, finding, treatment')
        for finding in findings:
            vulns = finding_dal.get_vulnerabilities(finding['finding_id'])
            for vuln in vulns:
                sheet.cell(row_index, vuln_where_col, vuln['where'])
                sheet.cell(row_index, vuln_specific_col, vuln['specific'])

                sheet.cell(row_index, project_col, project.upper())
                sheet.cell(row_index, finding_col, '{name!s} (#{id!s})'.format(
                           name=finding['finding'].encode('utf-8'),
                           id=finding['finding_id']))
                sheet.cell(row_index, treatment_col, finding['treatment'])
                sheet.cell(row_index, treatment_mgr_col,
                           vuln.get('treatment_manager', 'Unassigned'))

                row_index += 1

    username = user_data['user_email'].split('@')[0].encode('utf8', 'ignore')
    filename = 'complete_report.xlsx'
    filepath = '/tmp/{username}-{filename}'.format(filename=filename,
                                                   username=username)
    book.save(filepath)

    with open(filepath, 'rb') as document:
        response = HttpResponse(document.read())
        response['Content-Type'] = 'application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'inline;filename={filename}'.format(
            filename=filename)
    return response


@cache_content
@never_cache
def export_all_vulnerabilities(request):
    allowed_roles = ['admin']

    error = enforce_user_level_role(request, *allowed_roles)

    if error is not None:
        return error

    user_data = util.get_jwt_content(request)
    filepath = generate_all_vulns_xlsx(user_data['user_email'])
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as document:
        response = HttpResponse(document.read())
        response['Content-Type'] = 'application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'inline;filename={filename}'.format(
            filename=filename)
    return response


@cache_content
@never_cache
def export_users(request):  # pylint: disable=too-many-locals
    allowed_roles = ['admin']

    error = enforce_user_level_role(request, *allowed_roles)

    if error is not None:
        return error

    user_data = util.get_jwt_content(request)
    book = Workbook()
    sheet = book.active
    sheet.append(['full_name', 'user_email'])
    row_index = 2

    unique_users = []
    for user in user_dal.get_platform_users():
        user_email = user['user_email'].lower()
        if user_email not in unique_users:
            unique_users.append(user_email)

            name_attrs = user_domain.get_attributes(
                user_email, ['first_name', 'last_name'])
            full_name = ' '.join(list(name_attrs.values()))

            sheet.cell(row_index, 1, full_name)
            sheet.cell(row_index, 2, user_email)
            row_index += 1

    username = user_data['user_email'].split('@')[0].encode('utf8', 'ignore')
    filepath = f'/tmp/{username}-users.xlsx'
    filename = os.path.basename(filepath)
    book.save(filepath)

    with open(filepath, 'rb') as document:
        response = HttpResponse(document.read())
        response['Content-Type'] = 'application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = f'inline;filename={filename}'
    return response
