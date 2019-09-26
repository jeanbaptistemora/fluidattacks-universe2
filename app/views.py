# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=R1705
# pylint: disable=too-many-lines
""" Views and services for FluidIntegrates """

from __future__ import absolute_import
import os
import re
import sys
import time
from datetime import datetime, timedelta

import boto3
import rollbar
import yaml
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, condition
from jose import jwt
from magic import Magic
from openpyxl import load_workbook

from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
)
from app import util
from app.dal.helpers.drive import DriveAPI
from app.dal.helpers.formstack import FormstackAPI
from app.dal import integrates_dal
from app.decorators import authenticate, authorize, cache_content
from app.domain.vulnerability import (
    group_specific, get_open_vuln_by_type, get_vulnerabilities_by_type
)
from app.documentator.pdf import CreatorPDF
from app.documentator.secure_pdf import SecurePDF
from app.documentator.all_vulns import generate_all_vulns_xlsx
from app.dto import closing
from app.dto.finding import (
    FindingDTO, parse_finding, get_project_name,
    mask_finding_fields_dynamo
)
from app.services import (
    has_access_to_project, has_access_to_finding, has_access_to_event
)
from app.techdoc.IT import ITReport
from app.utils import reports

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

BUCKET_S3 = FI_AWS_S3_BUCKET
BASE_URL = "https://fluidattacks.com/integrates"


@never_cache
def index(request):
    "Login view for unauthenticated users"
    parameters = {}
    return render(request, "index.html", parameters)


def error500(request):
    "Internal server error view"
    parameters = {}
    return render(request, "HTTP500.html", parameters)


def error401(request):
    "Unauthorized error view"
    parameters = {}
    return render(request, "HTTP401.html", parameters)


@csrf_exempt
@cache_control(private=True, max_age=3600)
@authenticate
def app(request):
    """ App view for authenticated users """
    try:
        parameters = {
            'username': request.session['username']
        }
        response = render(request, 'app.html', parameters)
        token = jwt.encode(
            {
                'user_email': request.session['username'],
                'user_role': request.session['role'],
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
            httponly=True,
            max_age=settings.SESSION_COOKIE_AGE
        )
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return redirect('/error500')
    return response


@cache_control(private=True, max_age=3600)
@csrf_exempt
@authorize(['analyst', 'customer', 'customeradmin', 'admin'])
def dashboard(request):
    "View of control panel for authenticated users"
    try:
        parameters = {
            'username': request.session["username"],
            'company': request.session["company"],
            'last_login': request.session["last_login"]
        }
        integrates_dal.update_user_login(request.session["username"])
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return redirect('/error500')
    return render(request, "dashboard.html", parameters)


@csrf_exempt
@authenticate
def logout(request):
    "Close a user's active session"

    HttpResponse("<script>Intercom('shutdown');</script>")
    try:
        request.session.flush()
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)

    response = redirect("/index")
    response.delete_cookie(settings.JWT_COOKIE_NAME)
    return response


# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
@cache_content
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def project_to_xls(request, lang, project):
    "Create the technical report"
    findings_parsed = []
    detail = {
        "content_type": "application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet",
        "content_disposition": "inline;filename=:project.xlsx",
        "path": "/usr/src/app/app/autodoc/results/:project_:username.xlsx"
    }
    username = request.session['username'].split("@")[0]
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(request.session['username'],
                                 project, request.session['role']):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to export project xls without permission')
        return util.response([], 'Access denied', True)
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    findings = integrates_dal.get_findings_dynamo(project)
    if findings:
        for fin in findings:
            if util.validate_release_date(fin):
                finding_parsed = parse_finding(fin)
                finding = format_finding(finding_parsed, request)
                findings_parsed.append(finding)
            else:
                # Finding does not have a valid release date
                pass
    else:
        rollbar.report_message(
            'Error: project' + project + 'does not have findings in dynamo',
            'error',
            request)
        return util.response([], 'Empty fields', True)
    data = util.ord_asc_by_criticidad(findings_parsed)
    it_report = ITReport(project, data, username)
    filepath = it_report.result_filename
    reports.set_xlsx_password(filepath, time.strftime('%d%m%Y') + username)

    with open(filepath, 'r') as document:
        response = HttpResponse(document.read(),
                                content_type=detail["content_type"])
        file_name = detail["content_disposition"]
        file_name = file_name.replace(":project", project)
        response['Content-Disposition'] = file_name
    return response


def validation_project_to_pdf(request, lang, doctype):
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    if doctype not in ["tech", "executive"]:
        rollbar.report_message('Error: Unsupported doctype', 'error', request)
        return util.response([], 'Unsupported doctype', True)


# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
@cache_content
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def project_to_pdf(request, lang, project, doctype):
    "Export a project to a PDF"
    findings_parsed = []
    assert project.strip()
    if not has_access_to_project(request.session['username'],
                                 project, request.session['role']):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to export project pdf without permission')
        return util.response([], 'Access denied', True)
    else:
        user = request.session['username'].split("@")[0]
        validator = validation_project_to_pdf(request, lang, doctype)
        if validator is not None:
            return validator
        findings = integrates_dal.get_findings_dynamo(project)
        for fin in findings:
            if util.validate_release_date(fin):
                finding_parsed = parse_finding(fin)
                finding = format_finding(finding_parsed, request)
                findings_parsed.append(finding)
            else:
                # Finding does not have a valid release date
                pass
        pdf_maker = CreatorPDF(lang, doctype)
        secure_pdf = SecurePDF()
        findings_ord = util.ord_asc_by_criticidad(findings_parsed)
        findings = pdf_evidences(findings_ord)
        report_filename = ""
        if doctype == "tech":
            pdf_maker.tech(findings, project)
            report_filename = secure_pdf.create_full(user,
                                                     pdf_maker.out_name,
                                                     project)
        else:
            return HttpResponse("Disabled report generation",
                                content_type="text/html")
        if not os.path.isfile(report_filename):
            rollbar.report_message('Error: \
Documentation has not been generated', 'error', request)
            raise HttpResponse('Documentation has not been generated :(',
                               content_type="text/html")
        with open(report_filename, 'r') as document:
            response = HttpResponse(document.read(),
                                    content_type="application/pdf")
            response['Content-Disposition'] = \
                "inline;filename=:id.pdf".replace(":id", project + "_IT")
        return response


def pdf_evidences(findings):
    fin_dto = FindingDTO()
    for finding in findings:
        folder_name = finding['projectName'] + '/' + finding['id']
        key_list = key_existing_list(folder_name)
        field_list = [fin_dto.DOC_ACHV1, fin_dto.DOC_ACHV2,
                      fin_dto.DOC_ACHV3, fin_dto.DOC_ACHV4,
                      fin_dto.DOC_ACHV5]
        evidence_set = util.get_evidence_set_s3(finding, key_list, field_list)
        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                CLIENT_S3.download_file(
                    BUCKET_S3,
                    evidence['id'],
                    '/usr/src/app/app/documentator/images/' +
                    evidence['id'].split('/')[2])
                evidence['name'] = 'image::../images/' + \
                    evidence['id'].split('/')[2] + '[align="center"]'
        else:
            evidence_set = util.get_evidence_set(finding)
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                DriveAPI().download_images(evidence['id'])
                evidence['name'] = 'image::../images/' + \
                    evidence['id'] + '.png[align="center"]'
    return findings


def format_finding(finding, request):
    """Format some attributes in a finding."""
    finding_id = finding.get('id')
    finding_new = get_open_vuln_by_type(finding_id, request)
    finding['cardinalidad_total'] = finding.get('openVulnerabilities')
    finding['cierres'] = []
    if (finding_new and
            (finding_new.get('openVulnerabilities') or
                finding_new.get('closedVulnerabilities'))):
        finding = cast_new_vulnerabilities(finding_new, finding)
    else:
        if finding.get('where'):
            error_msg = \
                'Error: Finding {finding_id} of project {project} has \
vulnerabilities in old format'\
                .format(finding_id=finding_id, project=finding['projectName'])
            rollbar.report_message(error_msg, 'error', request)
        else:
            # Finding does not have vulnerabilities in old format.
            pass
        finding['estado'] = 'Abierto'
    finding = format_release_date(finding)
    if finding['estado'] == 'Cerrado':
        finding['where'] = '-'
        finding['treatmentManager'] = '-'
        finding['treatmentJustification'] = '-'
        finding['treatment'] = '-'
    return finding


def cast_new_vulnerabilities(finding_new, finding):
    """Cast values for new format."""
    total_cardinality = finding_new.get('openVulnerabilities') + \
        finding_new.get('closedVulnerabilities')
    finding['cardinalidad_total'] = str(total_cardinality)
    if (finding_new.get('closedVulnerabilities') > 0 and
            finding_new.get('openVulnerabilities') == 0):
        finding['estado'] = 'Cerrado'
    else:
        finding['estado'] = 'Abierto'
    if finding_new.get('openVulnerabilities') >= 0:
        finding['openVulnerabilities'] = \
            str(finding_new.get('openVulnerabilities'))
    else:
        # This finding does not have open vulnerabilities
        pass
    where = ''
    if finding_new.get('portsVulns'):
        finding['portsVulns'] = \
            group_specific(finding_new.get('portsVulns'), 'ports')
        where = format_where(where, finding['portsVulns'])
    else:
        # This finding does not have ports vulnerabilities
        pass
    if finding_new.get('linesVulns'):
        finding['linesVulns'] = \
            group_specific(finding_new.get('linesVulns'), 'lines')
        where = format_where(where, finding['linesVulns'])
    else:
        # This finding does not have lines vulnerabilities
        pass
    if finding_new.get('inputsVulns'):
        finding['inputsVulns'] = \
            group_specific(finding_new.get('inputsVulns'), 'inputs')
        where = format_where(where, finding['inputsVulns'])
    else:
        # This finding does not have inputs vulnerabilities
        pass
    finding['where'] = where
    return finding


def format_where(where, vulnerabilities):
    """Formate where field with new vulnerabilities."""
    for vuln in vulnerabilities:
        where = u'{where!s}{vuln_where!s} ({vuln_specific!s})\n'\
                .format(where=where,
                        vuln_where=vuln.get('where'),
                        vuln_specific=vuln.get('specific'))
    return where


def format_release_date(finding):
    primary_keys = ["finding_id", finding["id"]]
    table_name = "FI_findings"
    finding_dynamo = integrates_dal.get_data_dynamo(
        table_name, primary_keys[0], primary_keys[1])
    if finding_dynamo:
        if finding_dynamo[0].get("releaseDate"):
            finding["releaseDate"] = finding_dynamo[0].get("releaseDate")
        if finding_dynamo[0].get("lastVulnerability"):
            finding["lastVulnerability"] = \
                finding_dynamo[0].get("lastVulnerability")
    if finding.get("releaseDate"):
        final_date = util.calculate_datediff_since(finding["releaseDate"])
        finding['edad'] = final_date.days
        final_vuln_date = util.calculate_datediff_since(finding["lastVulnerability"])
        finding['lastVulnerability'] = final_vuln_date.days
    else:
        finding['lastVulnerability'] = '-'
    return finding


@cache_content
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def get_evidence(request, project, findingid, fileid):
    username = request.session['username']
    role = request.session['role']
    if (not has_access_to_finding(username, findingid, role) and
            not has_access_to_event(username, findingid, role)):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to retrieve evidence img without permission')
        return util.response([], 'Access denied', True)
    else:
        if fileid is None:
            rollbar.report_message('Error: Missing evidence image ID',
                                   'error', request)
            return HttpResponse("Error - Unsent image ID",
                                content_type="text/html")
        project = project.lower()
        key_list = key_existing_list(project + "/" + findingid + "/" + fileid)
        if key_list:
            for k in key_list:
                start = k.find(findingid) + len(findingid)
                localfile = "/tmp" + k[start:]
                ext = {'.png': '.tmp', '.gif': '.tmp'}
                localtmp = util.replace_all(localfile, ext)
                CLIENT_S3.download_file(BUCKET_S3, k, localtmp)
                return retrieve_image(request, localtmp)
        else:
            if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
                rollbar.report_message('Error: \
Invalid evidence image ID format', 'error', request)
                return HttpResponse("Error - ID with wrong format",
                                    content_type="text/html")
            else:
                drive_api = DriveAPI()
                evidence_img = drive_api.download(fileid)
                return retrieve_image(request, evidence_img)


@condition(etag_func=util.calculate_etag)
def retrieve_image(request, img_file):
    if util.assert_file_mime(img_file, ["image/png", "image/jpeg",
                                        "image/gif"]):
        with open(img_file, "r") as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return HttpResponse(file_obj.read(), content_type=mime_type)
    else:
        rollbar.report_message('Error: Invalid evidence image format',
                               'error', request)
        return HttpResponse("Error: Invalid evidence image format",
                            content_type="text/html")


def key_existing_list(key):
    """return the key's list if it exist, else list empty"""
    return util.list_s3_objects(CLIENT_S3, BUCKET_S3, key)


def delete_all_coments(finding_id):
    """Delete all comments of a finding."""
    all_comments = integrates_dal.get_comments_dynamo(int(finding_id), "comment")
    comments_deleted = [delete_comment(i) for i in all_comments]
    util.invalidate_cache(finding_id)
    return all(comments_deleted)


def delete_comment(comment):
    """Delete comment."""
    if comment:
        finding_id = comment["finding_id"]
        user_id = comment["user_id"]
        response = integrates_dal.delete_comment_dynamo(finding_id, user_id)
        util.invalidate_cache(finding_id)
    else:
        response = True
    return response


def delete_project(project):
    """Delete project information."""
    project = project.lower()
    util.invalidate_cache(project)
    are_users_removed = remove_all_users_access(project)
    is_project_masked = mask_project_findings(project)
    is_project_masked_in_dynamo = mask_project_findings_dynamo(project)
    are_closings_masked = mask_project_closings(project)
    project_deleted = remove_project_from_db(project)
    update_project_state_db = integrates_dal.update_attribute_dynamo(
        'FI_projects',
        ['project_name', project],
        'project_status', 'FINISHED')
    is_project_deleted = \
        are_users_removed and is_project_masked and \
        are_closings_masked and project_deleted and \
        is_project_masked_in_dynamo and update_project_state_db
    return is_project_deleted


def remove_all_users_access(project):
    """Remove user access to project."""
    all_users = integrates_dal.get_project_users(project)
    are_users_removed = True
    for user in all_users:
        is_user_removed = remove_user_access(project, user[0])
        if is_user_removed:
            are_users_removed = True
        else:
            are_users_removed = False
            break
    return are_users_removed


def remove_user_access(project, user_email):
    """Remove user access to project."""
    integrates_dal.remove_role_to_project_dynamo(project, user_email, "customeradmin")
    is_user_removed_dal = integrates_dal.remove_access_project(user_email,
                                                               project)
    is_user_removed_dynamo = integrates_dal.remove_project_access_dynamo(user_email, project)
    is_user_removed = is_user_removed_dal and is_user_removed_dynamo
    return is_user_removed


def mask_project_findings(project):
    """Mask project findings information."""
    api = FormstackAPI()
    try:
        finding_deleted = []
        finreqset = api.get_findings(project)['submissions']
        are_evidences_deleted = \
            [delete_s3_all_evidences(x['id'], project)
             for x in finreqset]
        finding_deleted.append(
            {"name": "S3", "was_deleted": all(are_evidences_deleted)})
        is_project_masked = list(map(mask_finding, finreqset))
        finding_deleted.append(
            {"name": "formstack", "was_deleted": all(is_project_masked)})
        are_comments_deleted = list(map(lambda x: delete_all_coments(x["id"]), finreqset))
        finding_deleted.append(
            {"name": "comments_dynamoDB", "was_deleted": all(are_comments_deleted)})
        integrates_dal.add_list_resource_dynamo(
            "FI_projects", "project_name", project, finding_deleted, "findings_deleted")
        is_project_deleted = all(is_project_masked) and all(are_evidences_deleted) \
            and all(are_comments_deleted)
        return is_project_deleted
    except KeyError:
        rollbar.report_message('Error: An error occurred masking project', 'error')
        return False


def mask_project_findings_dynamo(project):
    """Mask project findings information in DynamoDB."""
    api = FormstackAPI()
    fields = ['client_code', 'client_project', 'related_findings',
              'vulnerability', 'attack_vector_desc', 'affected_systems',
              'threat', 'risk', 'treatment_justification', 'treatment',
              'treatment_manager', 'effect_solution']
    try:
        finreqset = api.get_findings(project)["submissions"]
        are_findings_masked = list(map(
                                   lambda x:
                                   mask_finding_fields_dynamo(x['id'],
                                                              fields,
                                                              'Masked'), finreqset))
        is_project_deleted = all(are_findings_masked)
        deletion_track = [{"name": "description_dynamoDB", "was_deleted": is_project_deleted},
                          {"name": "vulns_dynamoDB", "was_deleted": is_project_deleted},
                          {"name": "evidence_dynamoDB", "was_deleted": is_project_deleted}]
        integrates_dal.add_list_resource_dynamo(
            "FI_projects", "project_name", project, deletion_track, "findings_deleted")
        return is_project_deleted
    except KeyError:
        rollbar.report_message('Error: An error occurred masking project in DynamoDB', 'error')
        return False


def mask_finding(submission_id):
    """Mask finding information."""
    api = FormstackAPI()
    finding_id = submission_id["id"]
    generic_dto = FindingDTO()
    generic_dto.mask_finding(finding_id, "Masked")
    generic_dto.to_formstack()
    request = api.update(generic_dto.request_id, generic_dto.data)
    return request


def mask_project_closings(project):
    """Mask project closings information."""
    api = FormstackAPI()
    try:
        closing_data = api.get_closings_by_project(project)["submissions"]
        masked = list(map(mask_closing, closing_data))
        is_closing_masked = all(masked)
        return is_closing_masked
    except KeyError:
        rollbar.report_message('Error: An error occurred masking closing', 'error')
        return False


def mask_closing(submission_id):
    """Mask closing information."""
    api = FormstackAPI()
    closing_id = submission_id["id"]
    closing_info = closing.mask_closing(closing_id, "Masked")["data"]
    request = api.update(closing_info['request_id'], closing_info["data"])
    return request


def delete_s3_all_evidences(finding_id, project):
    """Delete s3 evidences files."""
    evidences_list = key_existing_list(project + "/" + finding_id)
    is_evidence_deleted = False
    if evidences_list:
        is_evidence_deleted_s3 = list(map(delete_s3_evidence, evidences_list))
        is_evidence_deleted = any(is_evidence_deleted_s3)
    else:
        rollbar.report_message(
            'Warning: Finding {} does not have evidences in s3'.format(finding_id),
            'warning')
        is_evidence_deleted = True
    return is_evidence_deleted


def delete_s3_evidence(evidence):
    """Delete s3 evidence file."""
    try:
        response = CLIENT_S3.delete_object(Bucket=BUCKET_S3, Key=evidence)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200 or \
            response['ResponseMetadata']['HTTPStatusCode'] == 204
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def remove_project_from_db(project):
    """Delete records of projects in db."""
    deleted_mysql = integrates_dal.delete_project(project)
    return deleted_mysql


@cache_content
@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'admin'])
def download_vulnerabilities(request, findingid):
    """Download a file with all the vulnerabilities."""
    if not has_access_to_finding(request.session['username'], findingid,
                                 request.session['role']):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to retrieve vulnerabilities without permission')
        return util.response([], 'Access denied', True)
    else:
        finding = get_vulnerabilities_by_type(findingid)
        data_yml = {}
        vuln_types = {'ports': dict, 'lines': dict, 'inputs': dict}
        if finding:
            for vuln_key, cast_fuction in vuln_types.items():
                if finding.get(vuln_key):
                    data_yml[vuln_key] = list(map(cast_fuction, list(finding.get(vuln_key))))
                else:
                    # This finding does not have this type of vulnerabilities
                    pass
        else:
            # This finding does not have new vulnerabilities
            pass
        project = get_project_name(findingid).lower()
        file_name = '/tmp/{project}-{finding_id}.yaml'.format(
            finding_id=findingid, project=project)
        stream = file(file_name, 'w')
        yaml.safe_dump(data_yml, stream, default_flow_style=False)
        try:
            with open(file_name, 'r') as file_obj:
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
def generate_complete_report(request):
    user_data = util.get_jwt_content(request)
    projects = [project[0] for project in integrates_dal.get_projects_by_user(
        user_data['user_email'])]
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
        findings = integrates_dal.get_findings_released_dynamo(
            project, 'finding_id, finding, treatment, treatment_manager')
        for finding in findings:
            vulns = integrates_dal.get_vulnerabilities_dynamo(
                finding['finding_id'])
            for vuln in vulns:
                sheet.cell(row_index, vuln_where_col, vuln['where'])
                sheet.cell(row_index, vuln_specific_col, vuln['specific'])

                sheet.cell(row_index, project_col, project.upper())
                sheet.cell(row_index, finding_col, '{name!s} (#{id!s})'.format(
                           name=finding['finding'].encode('utf-8'),
                           id=finding['finding_id']))
                sheet.cell(row_index, treatment_col, finding['treatment'])
                sheet.cell(row_index, treatment_mgr_col,
                           finding.get('treatment_manager', 'Unassigned'))

                row_index += 1

    username = user_data['user_email'].split('@')[0].encode('utf8', 'ignore')
    filename = 'complete_report.xlsx'
    filepath = '/tmp/{username}-{filename}'.format(filename=filename,
                                                   username=username)
    book.save(filepath)

    with open(filepath, 'r') as document:
        response = HttpResponse(document.read())
        response['Content-Type'] = 'application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'inline;filename={filename}'.format(
            filename=filename)
    return response


@cache_content
@never_cache
@authorize(['admin'])
def export_all_vulnerabilities(request):
    user_data = util.get_jwt_content(request)
    filepath = generate_all_vulns_xlsx(user_data['user_email'])
    filename = os.path.basename(filepath)
    with open(filepath, 'r') as document:
        response = HttpResponse(document.read())
        response['Content-Type'] = 'application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'inline;filename={filename}'.format(
            filename=filename)
    return response
