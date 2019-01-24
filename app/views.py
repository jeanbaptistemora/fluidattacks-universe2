# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=R1705
""" Views and services for FluidIntegrates """

from __future__ import absolute_import
import os
import sys
import re
import pytz
import rollbar
import boto3
import yaml
import threading
from time import time
from django.conf import settings
from botocore.exceptions import ClientError
from django.shortcuts import render, redirect
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, condition
from django.http import HttpResponse
from jose import jwt
# pylint: disable=E0402
from . import util
from .decorators import (
    authenticate, authorize,
    require_project_access, require_finding_access,
    cache_content)
from .techdoc.IT import ITReport
from .domain import finding as finding_domain
from .dto.finding import (
    FindingDTO, format_finding_date, finding_vulnerabilities,
    sort_vulnerabilities, group_specific, update_vulnerabilities_date,
    save_severity, migrate_description, migrate_treatment, migrate_report_date,
    parse_dashboard_finding_dynamo, parse_finding, get_project_name
)
from .dto import closing
from .dto import project as project_dto
from .dto import eventuality
from .documentator.pdf import CreatorPDF
from .documentator.secure_pdf import SecurePDF
# pylint: disable=E0402
from .mailer import send_mail_delete_finding
from .mailer import send_mail_remediate_finding
from .mailer import send_mail_verified_finding
from .mailer import send_mail_delete_draft
from .mailer import send_mail_accepted_finding
from .services import (
    has_access_to_project, has_access_to_finding, has_access_to_event
)
from .services import is_customeradmin
from .utils import forms as forms_utils
from .dao import integrates_dao
from .api.drive import DriveAPI
from .api.formstack import FormstackAPI
from magic import Magic
from datetime import datetime, timedelta
from .entity import schema
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

client_s3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = FI_AWS_S3_BUCKET
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


@cache_control(private=True, max_age=3600)
@authenticate
@authorize(['analyst', 'admin'])
def forms(request):
    "Forms view"
    return render(request, "forms.html")


@cache_control(private=True, max_age=3600)
@authenticate
def project_indicators(request):
    "Indicators view"
    return render(request, "project/indicators.html")


@cache_control(private=True, max_age=3600)
@authenticate
def project_findings(request):
    "Project view"
    language = request.GET.get('l', 'en')
    dic_lang = {
        "search_findings": {
            "descriptions": {
                "description1": "",
                "description2": "Click",
                "description3": "on a finding to see more details"
            },
            "filter_buttons": {
                "advance": "Progress",
                "documentation": "Documentation"
            },
        }
    }
    if language == "es":
        dic_lang = {
            "search_findings": {
                "descriptions": {
                    "description1": "Haz",
                    "description2": "click",
                    "description3": "para ver mas detalles del hallazgo"
                },
                "filter_buttons": {
                    "advance": "Avance",
                    "documentation": "Documentacion"
                }
            }
        }
    return render(request, "project/findings.html", dic_lang)


@cache_control(private=True, max_age=3600)
@authenticate
@authorize(['analyst', 'admin'])
def project_drafts(request):
    "Drafts view"
    language = request.GET.get('l', 'en')
    dic_lang = {
        "search_findings": {
            "descriptions": {
                "description1": "",
                "description2": "Click",
                "description3": "on a finding to see more details"
            },
        }
    }
    if language == "es":
        dic_lang = {
            "search_findings": {
                "descriptions": {
                    "description1": "Haz",
                    "description2": "click",
                    "description3": "para ver mas detalles del hallazgo"
                }
            }
        }
    return render(request, "project/drafts.html", dic_lang)


@cache_control(private=True, max_age=3600)
@authenticate
def project_events(request):
    "eventualities view"
    language = request.GET.get('l', 'en')
    dic_lang = {
        "search_findings": {
            "eventualities": {
                "description": "Click on an event to see more details"
            },
            "event_by_name": {
                "btn_group": {
                    "resume": "Resume"
                }
            }
        }
    }
    if language == "es":
        dic_lang = {
            "search_findings": {
                "eventualities": {
                    "description": "Haz click para ver el detalle"
                },
                "event_by_name": {
                    "btn_group": {
                        "resume": "Resumen"
                    }
                }
            }
        }
    return render(request, "project/events.html", dic_lang)


@cache_control(private=True, max_age=3600)
@authenticate
def project_resources(request):
    "resources view"
    parameters = {}
    return render(request, "project/resources.html", parameters)


@cache_control(private=True, max_age=3600)
@authenticate
def project_users(request):
    "users view"
    parameters = {}
    return render(request, "project/users.html", parameters)


@cache_control(private=True, max_age=3600)
@authenticate
def project_comments(request):
    """ Project comments view """
    parameters = {}
    return render(request, 'project/comments.html', parameters)


@csrf_exempt
@cache_control(private=True, max_age=3600)
@authenticate
def registration(request):
    "Registry view for authenticated users"
    try:
        parameters = {
            'username': request.session["username"]
        }
        response = render(request, "registration.html", parameters)
        token = jwt.encode(
            {
                'user_email': request.session["username"],
                'user_role': request.session["role"],
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
        integrates_dao.update_user_login_dao(request.session["username"])
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
    findings = integrates_dao.get_findings_dynamo(project)
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
    with open(it_report.result_filename, 'r') as document:
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
    if doctype not in ["tech", "executive", "presentation"]:
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
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project',
                               'error', request)
        return util.response([], 'Empty fields', True)
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
        findings = integrates_dao.get_findings_dynamo(project)
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
        pdf_maker = CreatorPDF(lang, doctype)
        secure_pdf = SecurePDF()
        findings_ord = util.ord_asc_by_criticidad(findings_parsed)
        findings = pdf_evidences(findings_ord)
        report_filename = ""
        if doctype == "tech":
            pdf_maker.tech(findings, project, user)
            report_filename = secure_pdf.create_full(user,
                                                     pdf_maker.out_name,
                                                     project)
        elif doctype == "executive":
            return HttpResponse("Disabled report generation",
                                content_type="text/html")
        else:
            report_filename = presentation_pdf(project, pdf_maker,
                                               findings, user)
            if report_filename == "Incorrect parametrization":
                return HttpResponse("Incorrect parametrization",
                                    content_type="text/html")
            elif report_filename == "Incomplete documentation":
                return HttpResponse("Incomplete documentation",
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
                "inline;filename=:id.pdf".replace(":id", user + "_" + project)
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
                client_s3.download_file(
                    bucket_s3,
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


def presentation_pdf(project, pdf_maker, findings, user):
    project_info = get_project_info(project)["data"]
    mapa_id = util.drive_url_filter(project_info["findingsMap"])
    project_info["findingsMap"] = \
        "image::../images/"+mapa_id+'.png[align="center"]'
    DriveAPI().download_images(mapa_id)
    nivel_sec = project_info["securityLevel"].split(" ")[0]
    if not util.is_numeric(nivel_sec):
        return "Incorrect parametrization"
    nivel_sec = int(nivel_sec)
    if nivel_sec < 0 or nivel_sec > 6:
        return "Incorrect parametrization"
    project_info["securityLevel"] = \
        "image::../resources/presentation_theme/nivelsec"+str(nivel_sec)+'.png[align="center"]'
    if not project_info:
        return "Incomplete documentation"
    pdf_maker.presentation(findings, project, project_info, user)
    report_filename = pdf_maker.result_dir + pdf_maker.out_name
    return report_filename


# pylint: disable-msg=R0913
@cache_content
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def check_pdf(request, project):
    username = request.session['username']
    if not util.is_name(project):
        rollbar.report_message('Error: Name error in project',
                               'error', request)
        return util.response([], 'Name error', True)
    if not has_access_to_project(username, project, request.session['role']):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to export project pdf without permission')
        return util.response([], 'Access denied', True)
    reqset = get_project_info(project)
    if reqset:
        return util.response({"enable": True}, 'Success', False)
    return util.response({"enable": False}, 'Success', False)


def get_project_info(project):
    reqset = FormstackAPI().get_project_info(project)["submissions"]
    if reqset:
        submission_id = reqset[-1]["id"]
        submission = FormstackAPI().get_submission(submission_id)
        return project_dto.parse(submission)
    return []


@cache_content
@cache_control(private=True, max_age=3600)
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_finding_access
def get_finding(request):
    submission_id = request.POST.get('findingid', "")
    finding = integrates_dao.get_data_dynamo(
        'FI_findings',
        'finding_id',
        str(submission_id))
    if finding and finding[0].get('report_date'):
        finding_parsed = parse_finding(finding[0])
        finding = format_finding(finding_parsed, request)
    else:
        finding = catch_finding(request, submission_id)
    if finding is not None:
        if finding['vulnerability'].lower() == 'masked':
            util.cloudwatch_log(request, 'Warning: Project masked')
            return util.response([], 'Project masked', True)
        else:
            return util.response(finding, 'Success', False)
    else:
        util.cloudwatch_log(request,
                            'Finding with submission id: ' +
                            submission_id + ' not found')
        return util.response([], 'Error', True)


@cache_control(private=True, max_age=3600)
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'admin'])
@require_project_access
def get_drafts(request):
    """Capture and process the name of a project to return the drafts."""
    project = request.GET.get('project', "")
    api = FormstackAPI()
    findings = []
    finreqset = api.get_findings(project)["submissions"]
    for submission_id in finreqset:
        finding = catch_finding(request, submission_id["id"])
        if finding['vulnerability'].lower() == 'masked':
            util.cloudwatch_log(request, 'Warning: Project masked')
            return util.response([], 'Project masked', True)
        if finding['projectName'].lower() == project.lower() and \
                ('releaseDate' not in finding or
                    util.validate_future_releases(finding)):
            if finding.get("edad"):
                finding["releaseStatus"] = "Si"
            else:
                finding["releaseStatus"] = "No"
            findings.append(finding)
    return util.response(findings, 'Success', False)


@cache_content
@cache_control(private=True, max_age=3600)
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_findings(request):
    """Capture and process the name of a project to return the findings."""
    project = request.GET.get('project', "")
    project = project.lower()
    data_attr = "finding_id, records_number, vulnerability, \
                lastVulnerability, releaseDate, finding_type, treatment, \
                exploitability, confidentiality_impact, integrity_impact, \
                availability_impact, access_complexity, authentication, \
                access_vector, resolution_level, confidence_level, \
                project_name, finding"
    findings = integrates_dao.get_findings_dynamo(project, data_attr)
    findings_parsed = []
    for finding in findings:
        if (finding.get('vulnerability') and
                finding.get('vulnerability').lower() == 'masked'):
            util.cloudwatch_log(request, 'Warning: Project masked')
            return util.response([], 'Project masked', True)
        elif util.validate_release_date(finding):
            finding_parsed = parse_dashboard_finding_dynamo(finding)
            finding = format_finding(finding_parsed, request)
            findings_parsed.append(finding)
        else:
            rollbar.report_message('Error: \
An error occurred formatting finding', 'error', request)
    return util.response(findings_parsed, 'Success', False)


# pylint: disable=R1702
# pylint: disable=R0915
def catch_finding(request, submission_id):
    finding = []
    fin_dto = FindingDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        submission_data = api.get_submission(submission_id)
        if submission_data is None or 'error' in submission_data:
            return None
        else:
            finding = fin_dto.parse(
                submission_id,
                submission_data
            )
            finding = format_finding(finding, request)
            return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding',
                               'error', request)
        return None


def format_finding(finding, request):
    """Format some attributes in a finding."""
    finding_id = finding.get('id')
    query = """{
      finding(identifier: "findingid"){
        id
        success
        openVulnerabilities
        closedVulnerabilities
        portsVulns: vulnerabilities(
          vulnType: "ports", state: "open") {
          ...vulnInfo
        }
        linesVulns: vulnerabilities(
          vulnType: "lines", state: "open") {
          ...vulnInfo
        }
        inputsVulns: vulnerabilities(
          vulnType: "inputs", state: "open") {
          ...vulnInfo
        }
      }
    }
    fragment vulnInfo on Vulnerability {
      vulnType
      where
      specific
    }"""
    query = query.replace('findingid', finding_id)
    result = schema.SCHEMA.execute(query, context_value=request)
    finding_new = result.data.get('finding')
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
        finding['edad'] = '-'
        finding['lastVulnerability'] = '-'
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
            sort_vulnerabilities(finding_new.get('portsVulns'))
        where = format_where(where, finding['portsVulns'])
    else:
        # This finding does not have ports vulnerabilities
        pass
    if finding_new.get('linesVulns'):
        finding['linesVulns'] = \
            group_specific(finding_new.get('linesVulns'))
        where = format_where(where, finding['linesVulns'])
    else:
        # This finding does not have lines vulnerabilities
        pass
    if finding_new.get('inputsVulns'):
        finding['inputsVulns'] = \
            sort_vulnerabilities(finding_new.get('inputsVulns'))
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
    finding_dynamo = integrates_dao.get_data_dynamo(
        table_name, primary_keys[0], primary_keys[1])
    if finding_dynamo:
        if finding_dynamo[0].get("releaseDate"):
            finding["releaseDate"] = finding_dynamo[0].get("releaseDate")
        if finding_dynamo[0].get("lastVulnerability"):
            finding["lastVulnerability"] = \
                finding_dynamo[0].get("lastVulnerability")
    if finding.get("releaseDate"):
        final_date = format_finding_date(finding["releaseDate"])
        finding['edad'] = final_date.days
        final_vuln_date = format_finding_date(finding["lastVulnerability"])
        finding['lastVulnerability'] = final_vuln_date.days
    else:
        finding['lastVulnerability'] = '-'
    return finding


@cache_content
@cache_control(private=True, max_age=31536000)
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def get_evidence(request, project, findingid, fileid):
    username = request.session['username']
    role = request.session['role']
    if (not has_access_to_finding(username, findingid, role) or
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
                client_s3.download_file(bucket_s3, k, localtmp)
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
    return util.list_s3_objects(client_s3, bucket_s3, key)


def send_file_to_s3(filename, parameters, field, fieldname, ext, fileurl):
    fileroute = "/tmp/:id.tmp".replace(":id", filename)
    namecomplete = fileurl + "-" + field + "-" + filename + ext
    with open(fileroute, "r") as file_obj:
        try:
            client_s3.upload_fileobj(file_obj, bucket_s3, namecomplete)
        except ClientError:
            rollbar.report_exc_info()
            return False
    file_name = namecomplete.split("/")[2]
    is_file_saved = save_file_url(parameters['findingid'],
                                  fieldname, file_name)
    os.unlink(fileroute)
    return is_file_saved


def update_file_to_s3(parameters, field, fieldname, upload, fileurl):
    key_val = fileurl + "-" + field
    key_list = key_existing_list(key_val)
    if key_list:
        for k in key_list:
            client_s3.delete_object(Bucket=bucket_s3, Key=k)
    file_name_complete = fileurl + "-" + field + "-" + upload.name
    try:
        client_s3.upload_fileobj(upload.file, bucket_s3, file_name_complete)
        file_name = file_name_complete.split("/")[2]
        save_file_url(parameters['findingid'], fieldname, file_name)
        return False
    except ClientError:
        rollbar.report_exc_info()
        return True


def save_file_url(finding_id, field_name, file_url):
    file_data = []
    file_data.append({"name": field_name, "file_url": file_url})
    remove_file_url(finding_id, field_name)
    is_url_saved = integrates_dao.add_list_resource_dynamo(
        "FI_findings",
        "finding_id",
        finding_id,
        file_data,
        "files")
    return is_url_saved


def remove_file_url(finding_id, field_name):
    findings = integrates_dao.get_data_dynamo(
        "FI_findings",
        "finding_id",
        finding_id)
    for finding in findings:
        files = finding.get("files")
        if files:
            index = 0
            for file_obj in files:
                if file_obj.get("name") == field_name:
                    integrates_dao.remove_list_resource_dynamo(
                        "FI_findings",
                        "finding_id",
                        finding_id,
                        "files",
                        index)
                else:
                    message = \
                        'Info: Finding {finding!s} does not have {field!s} in s3' \
                        .format(finding=finding_id, field=field_name)
                    util.cloudwatch_log_plain(message)
                index += 1
        else:
            message = 'Info: Finding {finding!s} does not have evidences in s3' \
                .format(finding=finding_id)
            util.cloudwatch_log_plain(message)


def migrate_all_files(parameters, file_url, request):
    fin_dto = FindingDTO()
    try:
        api = FormstackAPI()
        frmreq = api.get_submission(parameters['findingid'])
        finding = fin_dto.parse(parameters['findingid'], frmreq)
        files = [{
            "id": "0",
            "name": "animation",
            "field": fin_dto.ANIMATION,
            "ext": ".gif"
        }, {
            "id": "1",
            "name": "exploitation",
            "field": fin_dto.EXPLOTATION,
            "ext": ".png"
        }, {
            "id": "2",
            "name": "evidence_route_1",
            "field": fin_dto.DOC_ACHV1,
            "ext": ".png"
        }, {
            "id": "3",
            "name": "evidence_route_2",
            "field": fin_dto.DOC_ACHV2,
            "ext": ".png"
        }, {
            "id": "4",
            "name": "evidence_route_3",
            "field": fin_dto.DOC_ACHV3,
            "ext": ".png"
        }, {
            "id": "5",
            "name": "evidence_route_4",
            "field": fin_dto.DOC_ACHV4,
            "ext": ".png"
        }, {
            "id": "6",
            "name": "evidence_route_5",
            "field": fin_dto.DOC_ACHV5,
            "ext": ".png"
        }, {
            "id": "7",
            "name": "exploit",
            "field": fin_dto.EXPLOIT,
            "ext": ".py"
        }, {
            "id": "8",
            "name": "fileRecords",
            "field": fin_dto.REG_FILE,
            "ext": ".csv"
        }]
        for file_obj in files:
            filename = '{file_url}-{field}'.format(file_url=file_url,
                                                   field=file_obj["field"])
            folder = key_existing_list(filename)
            if finding.get(file_obj["name"]) and \
                    parameters.get("id") != file_obj["id"] and not folder:
                file_id = finding[file_obj["name"]]
                fileroute = "/tmp/:id.tmp".replace(":id", file_id)
                if os.path.exists(fileroute):
                    send_file_to_s3(finding[file_obj["name"]],
                                    parameters,
                                    file_obj["field"],
                                    file_obj["name"],
                                    file_obj["ext"],
                                    file_url)
                else:
                    drive_api = DriveAPI()
                    file_download_route = drive_api.download(file_id)
                    if file_download_route:
                        send_file_to_s3(finding[file_obj["name"]],
                                        parameters,
                                        file_obj["field"],
                                        file_obj["name"],
                                        file_obj["ext"],
                                        file_url)
                    else:
                        rollbar.report_message(
                            'Error: An error occurred downloading file from Drive',
                            'error',
                            request)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)


@cache_content
@cache_control(private=True, max_age=3600)
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_myprojects(request):
    user = request.session["username"]
    data_set = integrates_dao.get_projects_by_user(user)
    json_data = []
    for row in data_set:
        json_data.append({
            "project": row[0].upper(),
            "company_project": row[1]
        })
    return util.response(json_data, 'Success', False)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
@require_finding_access
def update_description(request):
    parameters = request.POST.dict()
    finding_id = str(parameters['findingid'])
    project = get_project_name(finding_id)
    util.invalidate_cache(finding_id)
    util.invalidate_cache(project)
    try:
        generic_dto = FindingDTO()
        description_attributes = ['vulnerability']
        description = integrates_dao.get_finding_attributes_dynamo(
            finding_id,
            description_attributes)
        description_title = ['reportLevel', 'finding', 'probability', 'id',
                             'severity', 'riskValue', 'category', 'actor',
                             'scenario', 'recordsNumber', 'records',
                             'vulnerability', 'attackVector', 'affectedSystems',
                             'threat', 'requirements', 'cwe', 'effectSolution']
        finding = {k: parameters['data[' + k + ']']
                   for k in description_title
                   if parameters.get('data[' + k + ']')}
        if not description:
            api = FormstackAPI()
            submission_data = api.get_submission(finding_id)
            if submission_data is None or 'error' in submission_data:
                return util.response([], 'error', True)
            else:
                description_info = \
                    generic_dto.parse_description(submission_data, finding_id)
                project_info = \
                    generic_dto.parse_project(submission_data, finding_id)
                aditional_info = \
                    forms_utils.dict_concatenation(description_info,
                                                   project_info)
                finding = \
                    forms_utils.dict_concatenation(aditional_info, finding)
        else:
            # Finding have data in dynamo
            pass
        description_migrated = migrate_description(finding)
        migrate_report_date(finding)
        generic_dto.create_description(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request and description_migrated:
            return util.response([], 'success', False)
        else:
            rollbar.report_message('Error: \
An error occurred updating description', 'error', request)
            return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_finding_access
def update_treatment(request):
    parameters = request.POST.dict()
    try:
        project = get_project_name(parameters['data[id]'])
        util.invalidate_cache(parameters['data[id]'])
        util.invalidate_cache(project)
        description_title = ['id', 'treatment', 'treatmentJustification',
                             'treatmentManager', 'externalBts']
        finding = {k: parameters['data[' + k + ']']
                   for k in description_title
                   if parameters.get('data[' + k + ']')}
        request = migrate_treatment(finding)
        if request:
            if parameters['data[treatment]'] == 'Asumido':
                context = {
                    'user_mail': parameters['data[treatmentManager]'],
                    'finding_name': parameters['data[findingName]'],
                    'finding_id': parameters['data[id]'],
                    'project_name':
                        parameters['data[projectName]'].capitalize(),
                    'justification':
                        parameters['data[treatmentJustification]'],
                }
                project_name = parameters['data[projectName]'].lower()
                recipients = integrates_dao.get_project_users(project_name)
                to = [x[0] for x in recipients if x[1] == 1]
                email_send_thread = \
                    threading.Thread(name="Accepted finding email thread",
                                     target=send_mail_accepted_finding,
                                     args=(to, context,))
                email_send_thread.start()
                return util.response([], 'success', False)
            else:
                return util.response([], 'success', False)
        rollbar.report_message('Error: \
An error occurred updating treatment', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
@require_finding_access
def delete_finding(request):
    """Capture and process the ID of an eventuality to eliminate it"""
    submission_id = request.POST.get('findingid', "")
    parameters = request.POST.dict()
    util.invalidate_cache(submission_id)
    username = request.session['username']
    if not has_access_to_finding(request.session['username'],
                                 submission_id, request.session['role']):
        util.cloudwatch_log(request,
                            'Security: \
Attempted to delete findings without permission')
        return util.response([], 'Access denied', True)
    fin_dto = FindingDTO()
    try:
        context = fin_dto.create_delete(parameters,
                                        username, "", submission_id)
        api = FormstackAPI()
        frmreq = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmreq)
        context['project'] = finding['projectName']
        context["name_finding"] = finding["finding"]
        delete_all_coments(submission_id)
        delete_s3_all_evidences(submission_id, finding['projectName'].lower())
        integrates_dao.delete_finding_dynamo(submission_id)
        vulns = integrates_dao.get_vulnerabilities_dynamo(submission_id)
        for vuln in vulns:
            integrates_dao.delete_vulnerability_dynamo(vuln['UUID'],
                                                       submission_id)
        util.invalidate_cache(context['project'])
        result = api.delete_submission(submission_id)
        if result is None:
            rollbar.report_message('Error: An error ocurred deleting finding',
                                   'error', request)
            return util.response([], 'Error', True)
        to = ["projects@fluidattacks.com", "production@fluidattacks.com",
              "jarmas@fluidattacks.com", "smunoz@fluidattacks.com"]
        email_send_thread = \
            threading.Thread(name="Delete finding email thread",
                             target=send_mail_delete_finding,
                             args=(to, context,))
        email_send_thread.start()
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_finding_access
def finding_solved(request):
    """ Send an email requesting the verification of a finding """
    submission_id = request.POST.get('findingid', "")
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    remediated = integrates_dao.add_remediated_dynamo(
        int(submission_id),
        True,
        parameters['data[project]'],
        parameters['data[findingName]'])
    rem_solution = parameters['data[justification]'].replace('\n', ' ')
    finding_domain.add_comment(
        user_email=request.session['username'],
        parent='0',
        content=rem_solution,
        comment_type='comment',
        comment_id=int(round(time() * 1000)),
        finding_id=submission_id,
        user_fullname=str.join(' ', [request.session['first_name'],
                                     request.session['last_name']]),
        is_remediation_comment=True
    )
    util.invalidate_cache(submission_id)

    if not remediated:
        rollbar.report_message('Error: \
An error occurred when remediating the finding', 'error', request)
        return util.response([], 'Error', True)
    # Send email parameters
    try:
        to = [x[0] for x in recipients if x[1] == 1]
        to.append('continuous@fluidattacks.com')
        to.append('projects@fluidattacks.com')
        context = {
            'project': parameters['data[project]'],
            'finding_name': parameters['data[findingName]'],
            'user_mail': parameters['data[userMail]'],
            'finding_url': parameters['data[findingUrl]'],
            'finding_id': submission_id,
            'finding_vulns': parameters['data[findingVulns]'],
            'company': request.session["company"],
            'solution': rem_solution,
        }
        email_send_thread = \
            threading.Thread(name="Remediate finding email thread",
                             target=send_mail_remediate_finding,
                             args=(to, context,))
        email_send_thread.start()
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
@require_finding_access
def finding_verified(request):
    """ Send an email notifying that the finding was verified """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    verified = integrates_dao.add_remediated_dynamo(
        int(parameters['data[findingId]']),
        False, parameters['data[project]'],
        parameters['data[findingName]'])
    if not verified:
        rollbar.report_message('Error: \
An error occurred when verifying the finding', 'error', request)
        return util.response([], 'Error', True)
    analyst = request.session['username']
    update_vulnerabilities_date(analyst, parameters['data[findingId]'])
    # Send email parameters
    try:
        to = [x[0] for x in recipients if x[1] == 1]
        to.append('continuous@fluidattacks.com')
        to.append('projects@fluidattacks.com')
        context = {
            'project': parameters['data[project]'],
            'finding_name': parameters['data[findingName]'],
            'user_mail': parameters['data[userMail]'],
            'finding_url': parameters['data[findingUrl]'],
            'finding_id': parameters['data[findingId]'],
            'finding_vulns': parameters['data[findingVulns]'],
            'company': request.session["company"],
        }
        email_send_thread = \
            threading.Thread(name="Verified finding email thread",
                             target=send_mail_verified_finding,
                             args=(to, context,))
        email_send_thread.start()
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_finding_access
def get_remediated(request):
    finding_id = request.GET.get('findingid', "")
    remediated = integrates_dao.get_remediated_dynamo(int(finding_id))
    if remediated == []:
        return util.response({'remediated': False}, 'Success', False)
    resp = False
    for row in remediated:
        resp = row['remediated']
    return util.response({'remediated': resp}, 'Success', False)


@cache_control(private=True, max_age=3600)
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def total_severity(request):
    project = request.GET.get('project', "")
    toe = integrates_dao.get_toe_dynamo(project)
    return util.response(toe, 'Success', False)


@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
@require_finding_access
# pylint: disable=R0101
def accept_draft(request):
    parameters = request.POST.get('findingid', "")
    try:
        finding = catch_finding(request, parameters)
        if "releaseDate" not in finding:
            tzn = pytz.timezone('America/Bogota')
            release_date = datetime.now(tz=tzn).date()
            if ('subscription' in finding and
                (finding['subscription'] == 'Continua' or
                    finding['subscription'] == 'Concurrente' or
                    finding['subscription'] == 'Si')):
                releases = \
                    integrates_dao.get_project_dynamo(finding['projectName'].lower())
                for release in releases:
                    if "lastRelease" in release:
                        last_release = datetime.strptime(
                            release["lastRelease"].split(" ")[0],
                            '%Y-%m-%d'
                        )
                        last_release = last_release.replace(tzinfo=tzn).date()
                        if last_release == release_date:
                            release_date = release_date + timedelta(days=1)
                        elif last_release > release_date:
                            release_date = last_release + timedelta(days=1)
            release_date = release_date.strftime('%Y-%m-%d %H:%M:%S')
            release = {}
            release['id'] = parameters
            release['releaseDate'] = release_date
            primary_keys = ["finding_id", parameters]
            table_name = "FI_findings"
            has_release = integrates_dao.add_attribute_dynamo(
                table_name, primary_keys, "releaseDate", release_date)
            has_last_vuln = integrates_dao.add_attribute_dynamo(
                table_name, primary_keys, "lastVulnerability", release_date)
            finding['projectName'] = finding['projectName'].lower()
            if has_release and has_last_vuln:
                files_data = {'finding_id': parameters,
                              'project': finding['projectName']}
                file_first_name = '{project!s}-{findingid}'\
                    .format(project=files_data['project'],
                            findingid=files_data['finding_id'])
                file_url = '{project!s}/{findingid}/{file_name}'\
                    .format(project=files_data['project'],
                            findingid=files_data['finding_id'],
                            file_name=file_first_name)
                finding_domain.migrate_all_files(files_data, file_url, request)
                integrates_dao.add_release_toproject_dynamo(finding['projectName'],
                                                            True, release_date)
                save_severity(finding)
                migrate_description(finding)
                migrate_treatment(finding)
                migrate_report_date(finding)
                finding_domain.migrate_evidence_description(finding)
                util.invalidate_cache(finding['projectName'])
                util.invalidate_cache(parameters)
                return util.response([], 'success', False)
            else:
                rollbar.report_message('Error: \
An error occurred accepting the draft', 'error', request)
                return util.response([], 'error', True)
        else:
            util.cloudwatch_log(request, 'Security: \
Attempted to accept an already released finding')
            return util.response([], 'error', True)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
@require_finding_access
def delete_draft(request):
    submission_id = request.POST.get('findingid', "")
    util.invalidate_cache(submission_id)
    username = request.session['username']
    fin_dto = FindingDTO()
    try:
        finding_data = catch_finding(request, submission_id)
        if "releaseDate" not in finding_data:
            api = FormstackAPI()
            frmreq = api.get_submission(submission_id)
            finding = fin_dto.parse(submission_id, frmreq)
            context = {
                'project': finding['projectName'],
                'analyst_mail': finding['analyst'],
                'finding_name': finding['finding'],
                'admin_mail': username,
                'finding_id': submission_id,
            }
            result = api.delete_submission(submission_id)
            if result is None:
                rollbar.report_message('Error: \
An error ocurred deleting the draft', 'error', request)
                return util.response([], 'Error', True)
            delete_all_coments(submission_id)
            delete_s3_all_evidences(submission_id,
                                    finding['projectName'].lower())
            integrates_dao.delete_finding_dynamo(submission_id)
            vulns = integrates_dao.get_vulnerabilities_dynamo(submission_id)
            for vuln in vulns:
                integrates_dao.delete_vulnerability_dynamo(vuln['UUID'],
                                                           submission_id)
            admins = integrates_dao.get_admins()
            to = [x[0] for x in admins]
            to.append(finding['analyst'])
            email_send_thread = \
                threading.Thread(name="Delete draft email thread",
                                 target=send_mail_delete_draft,
                                 args=(to, context,))
            email_send_thread.start()
            return util.response([], 'success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


def delete_all_coments(finding_id):
    """Delete all comments of a finding."""
    all_comments = integrates_dao.get_comments_dynamo(int(finding_id), "comment")
    comments_deleted = [delete_comment(i) for i in all_comments]
    util.invalidate_cache(finding_id)
    return all(comments_deleted)


def delete_comment(comment):
    """Delete comment."""
    if comment:
        finding_id = comment["finding_id"]
        user_id = comment["user_id"]
        response = integrates_dao.delete_comment_dynamo(finding_id, user_id)
        util.invalidate_cache(finding_id)
    else:
        response = True
    return response


def calculate_indicators(project):
    api = FormstackAPI()
    event = eventuality.EventDTO()
    open_vulns = card_total = max_severity = open_events = 0
    for row in api.get_eventualities(project)["submissions"]:
        evtset = event.parse(row["id"], api.get_submission(row["id"]))
        if evtset['eventStatus'] == 'Pendiente':
            open_events += 1
    findings = integrates_dao.get_findings_dynamo(project, 'finding_id')
    for finding in findings:
        act_finding = finding_vulnerabilities(str(finding['finding_id']))
        open_vulns += int(act_finding['openVulnerabilities'])
        card_total += int(act_finding['cardinalidad_total'])
        if (max_severity < act_finding['criticity']):
            max_severity = act_finding['criticity']
    try:
        fixed_vuln = int(round((1.0 - (float(open_vulns) / float(card_total)))*100.0))
    except ZeroDivisionError:
        fixed_vuln = 0
    return [open_events, max_severity, fixed_vuln]


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def is_customer_admin(request):
    project = request.GET.get('project', "")
    email = request.GET.get('email', "")
    try:
        if is_customeradmin(project, email):
            return util.response(True, 'Success', False)
        return util.response(False, 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response(False, 'Error', True)


@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def access_to_project(request):
    project = request.GET.get('project', "")
    if has_access_to_project(request.session['username'], project, request.session['role']):
        return util.response(True, 'success', False)
    return util.response(False, 'success', False)


def delete_project(project):
    """Delete project information."""
    project = project.lower()
    util.invalidate_cache(project)
    are_users_removed = remove_all_users_access(project)
    is_project_masked = mask_project_findings(project)
    are_closings_masked = mask_project_closings(project)
    project_deleted = remove_project_from_db(project)
    is_project_deleted = are_users_removed and is_project_masked \
        and are_closings_masked and project_deleted
    return is_project_deleted


def remove_all_users_access(project):
    """Remove user access to project."""
    all_users = integrates_dao.get_project_users(project)
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
    integrates_dao.remove_role_to_project_dynamo(project, user_email, "customeradmin")
    is_user_removed_dao = integrates_dao.remove_access_project_dao(user_email,
                                                                   project)
    is_user_removed_dynamo = integrates_dao.remove_project_access_dynamo(user_email, project)
    is_user_removed = is_user_removed_dao and is_user_removed_dynamo
    return is_user_removed


def mask_project_findings(project):
    """Mask project findings information."""
    api = FormstackAPI()
    try:
        finding_deleted = []
        finreqset = api.get_findings(project)["submissions"]
        are_evidences_deleted = list(map(lambda x: delete_s3_all_evidences(x["id"], project), finreqset))
        finding_deleted.append(
            {"name": "S3", "was_deleted": all(are_evidences_deleted)})
        is_project_masked = list(map(mask_finding, finreqset))
        finding_deleted.append(
            {"name": "formstack", "was_deleted": all(is_project_masked)})
        are_comments_deleted = list(map(lambda x: delete_all_coments(x["id"]), finreqset))
        finding_deleted.append(
            {"name": "comments_dynamoDB", "was_deleted": all(are_comments_deleted)})
        are_vuln_deleted = list(map(lambda x: delete_vulnerabilities(x["id"], project), finreqset))
        integrates_dao.add_list_resource_dynamo(
            "FI_projects", "project_name", project, finding_deleted, "findings_deleted")
        is_project_deleted = all(is_project_masked) and all(are_evidences_deleted) \
            and all(are_comments_deleted) and all(are_vuln_deleted)
        return is_project_deleted
    except KeyError:
        rollbar.report_message('Error: An error occurred masking project', 'error')
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
        util.cloudwatch_log_plain(
            'Info: Finding ' + finding_id + ' does not have evidences in s3')
        is_evidence_deleted = True
    return is_evidence_deleted


def delete_s3_evidence(evidence):
    """Delete s3 evidence file."""
    try:
        response = client_s3.delete_object(Bucket=bucket_s3, Key=evidence)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200 or \
            response['ResponseMetadata']['HTTPStatusCode'] == 204
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def remove_project_from_db(project):
    """Delete records of projects in db."""
    deleted_mysql = integrates_dao.delete_project(project)
    return deleted_mysql


def delete_vulnerabilities(finding_id, project):
    """Delete vulnerabilities from dynamo."""
    are_vulns_deleted = integrates_dao.delete_vulns_email_dynamo(project, finding_id)
    return are_vulns_deleted


@cache_content
@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'admin'])
def download_vulnerabilities(request, findingid):
    """Download a file with all the vulnerabilities."""
    if not has_access_to_finding(request.session['username'], findingid, request.session['role']):
        util.cloudwatch_log(request, 'Security: Attempted to retrieve vulnerabilities without permission')
        return util.response([], 'Access denied', True)
    else:
        query = """{
          finding(identifier: "findingid") {
            id
            success
            openVulnerabilities
            closedVulnerabilities
            ports: vulnerabilities(vulnType: "ports") {
              host: where
              port: specific
              state: currentState
            }
            lines: vulnerabilities(vulnType: "lines") {
              path: where
              line: specific
              state: currentState
            }
            inputs: vulnerabilities(vulnType: "inputs") {
              url: where
              field: specific
              state: currentState
            }
          }
        }"""
        query = query.replace('findingid', findingid)
        result = schema.SCHEMA.execute(query, context_value=request)
        finding = result.data.get('finding')
        data_yml = {}
        vuln_types = {'ports': cast_ports, 'lines': dict, 'inputs': dict}
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
        file_name = '/tmp/vulnerabilities{findingid}.yaml'.format(findingid=findingid)
        stream = file(file_name, 'w')
        yaml.safe_dump(data_yml, stream, default_flow_style=False)
        try:
            with open(file_name, 'r') as file_obj:
                response = HttpResponse(file_obj.read(), content_type='text/x-yaml')
                response['Content-Disposition'] = 'attachment; filename="vulnerabilities.yaml"'
                return response
        except IOError:
            rollbar.report_message('Error: Invalid vulnerabilities file format', 'error', request)
            return util.response([], 'Invalid vulnerabilities file format', True)


def cast_ports(ports):
    """Cast ports to be int."""
    ports = dict(ports)
    ports['port'] = int(ports['port'])
    return ports
