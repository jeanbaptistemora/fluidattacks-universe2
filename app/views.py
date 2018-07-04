# -*- coding: utf-8 -*-
""" Views and services for FluidIntegrates """

from __future__ import absolute_import
import os
import sys
import re
import pytz
import rollbar
import boto3
import io
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from botocore.exceptions import ClientError
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize, require_project_access
from .techdoc.IT import ITReport
from .dto.finding import FindingDTO
from .dto.closing import ClosingDTO
from .dto.project import ProjectDTO
from .dto.eventuality import EventualityDTO
from .documentator.pdf import CreatorPDF
from .documentator.secure_pdf import SecurePDF
# pylint: disable=E0402
from .mailer import send_mail_delete_finding
from .mailer import send_mail_remediate_finding
from .mailer import send_mail_new_comment
from .mailer import send_mail_reply_comment
from .mailer import send_mail_verified_finding
from .mailer import send_mail_reject_release
from .mailer import send_mail_access_granted
from .services import has_access_to_project
from .services import is_customeradmin
from .dao import integrates_dao
from .api.drive import DriveAPI
from .api.formstack import FormstackAPI
from magic import Magic
from datetime import datetime, timedelta
from backports import csv
from .entity.query import Query
from graphene import Schema
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET

client_s3 = boto3.client('s3',
                            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = FI_AWS_S3_BUCKET

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

@never_cache
@authenticate
@authorize(['analyst', 'admin'])
def forms(request):
    "Forms view"
    return render(request, "forms.html")

@never_cache
@authenticate
def project_indicators(request):
    "Indicators view"
    return render(request, "project/indicators.html")

@never_cache
@authenticate
def project_findings(request):
    "Project view"
    language = request.GET.get('l', 'en')
    dicLang = {
        "search_findings": {
            "headings": {
                "action": "Action",
                "age": "Age (Days)",
                "cardinality": "Open Vuln.",
                "criticity": "Severity",
                "exploit": "Exploitable",
                "finding": "Title",
                "lastVulnerability": "Last Report (Days)",
                "state": "Status",
                "timestamp": "Date",
                "treatment": "Treatment",
                "type": "Type",
                "vulnerability": "Description"
            },
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
        dicLang = {
            "search_findings": {
                "headings": {
                    "action": "Accion",
                    "age": "Edad (Días)",
                    "cardinality": "Vuln. Abiertas",
                    "criticity": "Severidad",
                    "exploit": "Explotable",
                    "finding": "Titulo",
                    "lastVulnerability": "Último Reporte (Días)",
                    "state": "Estado",
                    "timestamp": "Fecha",
                    "treatment": "Tratamiento",
                    "type": "Tipo",
                    "vulnerability": "Descripcion"
                },
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
    return render(request, "project/findings.html", dicLang)

@never_cache
@authenticate
@authorize(['analyst', 'admin'])
def project_releases(request):
    "Releases date of findings"
    language = request.GET.get('l', 'en')
    dicLang = {
        "search_findings": {
            "headings": {
                "action": "Action",
                "age": "Age (Days)",
                "cardinality": "Open Vuln.",
                "criticity": "Severity",
                "exploit": "Exploitable",
                "finding": "Title",
                "lastVulnerability": "Last Report (Days)",
                "state": "Status",
                "timestamp": "Date",
                "treatment": "Treatment",
                "type": "Type",
                "vulnerability": "Description"
            },
            "descriptions": {
                "description1": "",
                "description2": "Click",
                "description3": "on a finding to see more details"
            },
            "filter_buttons": {
               "advance": "Progress"
            },
        }
    }
    if language == "es":
        dicLang = {
            "search_findings": {
                "headings": {
                    "action": "Accion",
                    "age": "Edad (Días)",
                    "cardinality": "Vuln. Abiertas",
                    "criticity": "Severidad",
                    "exploit": "Explotable",
                    "finding": "Titulo",
                    "lastVulnerability": "Último Reporte (Días)",
                    "state": "Estado",
                    "timestamp": "Fecha",
                    "treatment": "Tratamiento",
                    "type": "Tipo",
                    "vulnerability": "Descripcion"
                },
                "descriptions": {
                    "description1": "Haz",
                    "description2": "click",
                    "description3": "para ver mas detalles del hallazgo"
                },
                "filter_buttons": {
                   "advance": "Avance"
                }
            }
        }
    return render(request, "project/releases.html", dicLang)

@never_cache
@authenticate
def project_events(request):
    "eventualities view"
    language = request.GET.get('l', 'en')
    dicLang = {
        "search_findings": {
            "event_table": {
               "date": "Date",
               "details": "Description",
               "id": "ID",
               "status": "Status",
               "type": "Type"
            },
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
        dicLang = {
            "search_findings": {
                "event_table": {
                   "date": "Fecha",
                   "details": "Descripción",
                   "id": "ID",
                   "status": "Estado",
                   "type": "Tipo"
                },
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
    return render(request, "project/events.html", dicLang)

@never_cache
@authenticate
def project_users(request):
    language = request.GET.get('l', 'en')
    dicLang = {
        "search_findings": {
            "users_table": {
               "userOrganization": "Organization",
               "usermail": "User email",
               "firstlogin": "First login",
               "lastlogin": "Last login",
               "userRole": "Role"
            },
        }
    }
    if language == "es":
        dicLang = {
            "search_findings": {
                "users_table": {
                   "userOrganization": "Organización",
                   "usermail": "Email",
                   "firstlogin": "Primer ingreso",
                   "lastlogin": "Último ingreso",
                   "userRole": "Rol"
                },
            }
        }
    return render(request, "project/users.html", dicLang)

@csrf_exempt
@never_cache
@authenticate
def registration(request):
    "Registry view for authenticated users"
    try:
        parameters = {
            'username': request.session["username"]
        }
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return redirect('/error500')
    return render(request, "registration.html", parameters)

@never_cache
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
        if 'legal_status' in request.session:
            parameters['legal_status'] = request.session['legal_status']
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
    return redirect("/index")

#pylint: disable=too-many-branches
#pylint: disable=too-many-locals
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def project_to_xls(request, lang, project):
    "Create the technical report"
    findings = []
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
    if not has_access_to_project(request.session['username'], project, request.session['role']):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response([], 'Access denied', True)
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    for reqset in FormstackAPI().get_findings(project)["submissions"]:
        fin = catch_finding(request, reqset["id"])
        if fin['fluidProject'].lower() == project.lower() and \
                'releaseDate' in fin:
            tzn = pytz.timezone('America/Bogota')
            today_day = datetime.now(tz=tzn).date()
            finding_last_vuln = datetime.strptime(
                fin["releaseDate"].split(" ")[0],
                '%Y-%m-%d'
            )
            finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
            if finding_last_vuln <= today_day:
                findings.append(fin)
    data = util.ord_asc_by_criticidad(findings)
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

#pylint: disable=too-many-branches
#pylint: disable=too-many-locals
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def project_to_pdf(request, lang, project, doctype):
    "Export a project to a PDF"
    findings = []
    user = request.session['username'].split("@")[0]
    validator = validation_project_to_pdf(request, lang, doctype)
    if validator is not None:
        return validator
    for reqset in FormstackAPI().get_findings(project)["submissions"]:
        fin = catch_finding(request, reqset["id"])
        if fin['fluidProject'].lower() == project.lower() and \
                'releaseDate' in fin:
            tzn = pytz.timezone('America/Bogota')
            today_day = datetime.now(tz=tzn).date()
            finding_last_vuln = datetime.strptime(
                fin["releaseDate"].split(" ")[0],
                '%Y-%m-%d'
            )
            finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
            if finding_last_vuln <= today_day:
                findings.append(fin)
    pdf_maker = CreatorPDF(lang, doctype)
    secure_pdf = SecurePDF()
    findings = util.ord_asc_by_criticidad(findings)
    report_filename = ""
    for finding in findings:
        key_list = key_existing_list(finding['id'])
        field_list = [FindingDTO().DOC_ACHV1, FindingDTO().DOC_ACHV2, \
                    FindingDTO().DOC_ACHV3, FindingDTO().DOC_ACHV4, \
                    FindingDTO().DOC_ACHV5]
        evidence_set = util.get_evidence_set_s3(finding, key_list, field_list)
        if evidence_set:
            finding["evidence_set"] = evidence_set
            for evidence in evidence_set:
                client_s3.download_file(bucket_s3, \
                                        finding['id'] + "/" + evidence["id"], \
                                        "/usr/src/app/app/documentator/images/" + evidence["id"])
                evidence['name'] = "image::../images/"+evidence["id"]+'[align="center"]'
        else:
            evidence_set = util.get_evidence_set(finding)
            finding["evidence_set"] = evidence_set
            for evidence in evidence_set:
                DriveAPI().download_images(evidence["id"])
                evidence["name"] = "image::../images/"+evidence["id"]+'.png[align="center"]'
    if doctype == "tech":
        pdf_maker.tech(findings, project, user)
        report_filename = secure_pdf.create_full(user, pdf_maker.out_name)
    elif doctype == "executive":
        return HttpResponse("Disabled report generation", content_type="text/html")
    else:
        project_info = get_project_info(project)
        mapa_id = util.drive_url_filter(project_info["findingsMap"])
        project_info["findingsMap"] = "image::../images/"+mapa_id+'.png[align="center"]'
        DriveAPI().download_images(mapa_id)
        nivel_sec = project_info["securityLevel"].split(" ")[0]
        if not util.is_numeric(nivel_sec):
            return HttpResponse("Incorrect parametrization", content_type="text/html")
        nivel_sec = int(nivel_sec)
        if nivel_sec < 0 or nivel_sec > 6:
            return HttpResponse("Incorrect parametrization", content_type="text/html")
        project_info["securityLevel"] = "image::../resources/presentation_theme/nivelsec"+str(nivel_sec)+'.png[align="center"]'
        print project_info
        if not project_info:
            return HttpResponse("Incomplete documentation", content_type="text/html")
        pdf_maker.presentation(findings, project, project_info, user)
        #secure_pdf = SecurePDF()
        #report_filename = secure_pdf.create_only_pass(user, pdf_maker.out_name)
        report_filename = pdf_maker.RESULT_DIR + pdf_maker.out_name
    if not os.path.isfile(report_filename):
        rollbar.report_message('Error: Documentation has not been generated', 'error', request)
        raise HttpResponse('Documentation has not been generated :(', content_type="text/html")
    with open(report_filename, 'r') as document:
        response = HttpResponse(document.read(),
                                content_type="application/pdf")
        response['Content-Disposition'] = \
            "inline;filename=:id.pdf".replace(":id", user + "_" + project)
    return response

#pylint: disable-msg=R0913
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def check_pdf(request, project):
    username = request.session['username']
    if not util.is_name(project):
        rollbar.report_message('Error: Name error in project', 'error', request)
        return util.response([], 'Name error', True)
    if not has_access_to_project(username, project, request.session['role']):
        rollbar.report_message('Error: Access to project denied', 'error', request)
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
        return ProjectDTO().parse(submission)
    return []

#pylint: disable-msg=R1705
@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_eventualities(request):
    "Get the eventualities of a project."
    project = request.GET.get('project', None)
    category = request.GET.get('category', None)
    username = request.session['username']
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    if category == "Name":
        submissions = api.get_eventualities(project)
        if 'error' not in submissions:
            frmset = submissions["submissions"]
            for row in frmset:
                submission = api.get_submission(row["id"])
                evtset = evt_dto.parse(row["id"], submission)
                if evtset['fluidProject'].lower() == project.lower():
                    dataset.append(evtset)
            return util.response(dataset, 'Success', False)
        else:
            return util.response(dataset, 'Event does not exist', True)
    elif category == "ID":
        # Only fluid can filter by id
        if "@fluidattacks.com" not in username:
            rollbar.report_message('Error: Access to project denied', 'error', request)
            return util.response(dataset, 'Access to project denied', True)
        if not project.isdigit():
            rollbar.report_message('Error: ID is not a number', 'error', request)
            return util.response(dataset, 'ID is not a number', True)
        submission = api.get_submission(project)
        if 'error' not in submission:
            evtset = evt_dto.parse(project, submission)
            dataset.append(evtset)
            return util.response(dataset, 'Success', False)
        else:
            return util.response(dataset, 'Event does not exist', True)
    else:
        rollbar.report_message('Error: An error occurred getting events', 'error', request)
        return util.response(dataset, 'Not actions', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_users_login(request):
    "Get the email and last login date of all users in a project."
    project = request.GET.get('project', None)
    dataset = []
    actualUser = request.session['username']
    if request.session['role'] == 'customer' and not is_customeradmin(project, actualUser):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response(dataset, 'Access to project denied', True)
    initialEmails = integrates_dao.get_project_users(project.lower())
    initialEmailsList = [x[0] for x in initialEmails if x[1] == 1]
    usersEmail = util.user_email_filter(initialEmailsList, actualUser)
    for user in usersEmail:
        data = {}
        last_login = integrates_dao.get_user_last_login_dao(user)
        last_login = last_login.split('.',1)[0]
        if last_login == "1111-01-01 11:11:11":
            data['usersLogin']=[-1,-1]
        else:
            dates_difference = datetime.now()-datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
            diff_last_login=[dates_difference.days,dates_difference.seconds]
            data['usersLogin']=diff_last_login
        first_login = integrates_dao.get_user_first_login_dao(user)
        first_login = first_login.split('.',1)[0]
        data['users']=user
        data['usersFirstLogin']=first_login
        data['usersOrganization']=integrates_dao.get_organization_dao(user).title()
        userRole=integrates_dao.get_role_dao(user)
        if is_customeradmin(project, user):
            data['userRole'] = "customer_admin"
        elif userRole == "customeradmin":
            data['userRole'] = "customer"
        else:
            data['userRole'] = userRole
        dataset.append(data)
    return util.response(dataset, 'Success', False)


@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_finding(request):
    submission_id = request.POST.get('id', "")
    finding = catch_finding(request, submission_id)
    if not finding is None:
        if finding['vulnerability'].lower() == 'masked':
            rollbar.report_message('Warning: Project masked', 'warning', request)
            return util.response([], 'Project masked', True)
        if finding:
            return util.response(finding, 'Success', False)
    return util.response([], 'Wrong', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'admin'])
@require_project_access
# pylint: disable=R0912
# pylint: disable=R0914
def get_releases(request):
    """Capture and process the name of a project to return the releases."""
    project = request.GET.get('project', "")
    api = FormstackAPI()
    findings = []
    finreqset = api.get_findings(project)["submissions"]
    for submission_id in finreqset:
        finding = catch_finding(request, submission_id["id"])
        if finding['vulnerability'].lower() == 'masked':
            rollbar.report_message('Warning: Project masked', 'warning', request)
            return util.response([], 'Project masked', True)
        if finding['fluidProject'].lower() == project.lower() and \
                'releaseDate' not in finding:
            findings.append(finding)
    return util.response(findings, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
# pylint: disable=R0912
# pylint: disable=R0914
def get_findings(request):
    """Capture and process the name of a project to return the findings."""
    project = request.GET.get('project', "").encode('utf-8')
    api = FormstackAPI()
    findings = []
    finreqset = api.get_findings(project)["submissions"]
    for submission_id in finreqset:
        finding = catch_finding(request, submission_id["id"])
        if not finding is None:
            if finding['vulnerability'].lower() == 'masked':
                rollbar.report_message('Warning: Project masked', 'warning', request)
                return util.response([], 'Project masked', True)
            if finding['fluidProject'].lower() == project.lower() and \
                    'releaseDate' in finding:
                tzn = pytz.timezone('America/Bogota')
                today_day = datetime.now(tz=tzn).date()
                finding_last_vuln = datetime.strptime(
                    finding["releaseDate"].split(" ")[0],
                    '%Y-%m-%d'
                )
                finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
                if finding_last_vuln <= today_day:
                    findings.append(finding)
    import json
    with open("/tmp/"+project+".txt", "w") as f:
        f.write(json.dumps(findings))
    return util.response(findings, 'Success', False)

# pylint: disable=R1702
# pylint: disable=R0915
def catch_finding(request, submission_id):
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        submissionData = api.get_submission(submission_id)
        if submissionData is None or 'error' in submissionData:
            return None
        else:
            finding = fin_dto.parse(
                submission_id,
                submissionData,
                request
            )
            closingData = api.get_closings_by_id(submission_id)
            if closingData is None or 'error' in closingData:
                return None
            else:
                closingreqset = closingData["submissions"]
                findingcloseset = []
                for closingreq in closingreqset:
                    closingset = cls_dto.parse(api.get_submission(closingreq["id"]))
                    findingcloseset.append(closingset)
                    # The latest is the last closing cycle.
                    state = closingset
                finding["estado"] = state["estado"]
                finding["cierres"] = findingcloseset
                finding['cardinalidad_total'] = finding['openVulnerabilities']
                if 'opened' in state:
                    # Hack: This conditional temporarily solves the problem presented
                    #      when the number of vulnerabilities open in a closing cycle
                    # are higher than the number of vulnerabilities open in a finding
                    # which causes negative numbers to be shown in the indicators view.
                    if int(state['opened']) > int(finding['cardinalidad_total']):
                        finding['cardinalidad_total'] = state['opened']
                    finding['openVulnerabilities'] = state['opened']
                if 'whichOpened' in state:
                    finding['where'] = state['whichOpened']
                else:
                    if state['estado'] == 'Cerrado':
                        finding['where'] = '-'
                if 'whichClosed' in state:
                    finding['closed'] = state['whichClosed']
                if state['estado'] == 'Cerrado':
                    finding['where'] = '-'
                    finding['edad'] = '-'
                    finding['lastVulnerability'] = '-'
                else:
                    if 'timestamp' in state:
                        if 'lastVulnerability' in finding and \
                                finding['lastVulnerability'] != state['timestamp']:
                            finding['lastVulnerability'] = state['timestamp']
                            generic_dto = FindingDTO()
                            generic_dto.create_last_vulnerability(finding)
                            generic_dto.to_formstack()
                            api.update(generic_dto.request_id, generic_dto.data)
                    if 'releaseDate' in finding:
                        tzn = pytz.timezone('America/Bogota')
                        finding_date = datetime.strptime(
                            finding["releaseDate"].split(" ")[0],
                            '%Y-%m-%d'
                        )
                        finding_date = finding_date.replace(tzinfo=tzn).date()
                        final_date = (datetime.now(tz=tzn).date() - finding_date)
                        finding['edad'] = ":n".replace(":n", str(final_date.days))
                        finding_last_vuln = datetime.strptime(
                            finding["lastVulnerability"].split(" ")[0],
                            '%Y-%m-%d'
                        )
                        finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
                        final_vuln_date = (datetime.now(tz=tzn).date() - finding_last_vuln)
                        finding['lastVulnerability'] = ":n".replace(":n", str(final_vuln_date.days))
                    else:
                        finding['lastVulnerability'] = '-'
                return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error', request)
        return None

def finding_vulnerabilities(submission_id):
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        finding = fin_dto.parse_vulns_by_id(
            submission_id,
            api.get_submission(submission_id)
        )
        closingreqset = api.get_closings_by_id(submission_id)["submissions"]
        findingcloseset = []
        for closingreq in closingreqset:
            closingset = cls_dto.parse(api.get_submission(closingreq["id"]))
            findingcloseset.append(closingset)
            state = closingset
        finding["estado"] = state["estado"]
        finding["cierres"] = findingcloseset
        finding['cardinalidad_total'] = finding['openVulnerabilities']
        if 'opened' in state:
            finding['openVulnerabilities'] = state['opened']
        else:
            if state['estado'] == 'Cerrado':
                finding['where'] = '-'
        if state['estado'] == 'Cerrado':
            finding['where'] = '-'
            finding['edad'] = '-'
        elif 'releaseDate' in finding:
            tzn = pytz.timezone('America/Bogota')
            today_day = datetime.now(tz=tzn).date()
            finding_last_vuln = datetime.strptime(
                finding["releaseDate"].split(" ")[0],
                '%Y-%m-%d'
            )
            finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
            if finding_last_vuln <= today_day:
                finding_date = datetime.strptime(
                    finding["releaseDate"].split(" ")[0],
                    '%Y-%m-%d'
                )
                finding_date = finding_date.replace(tzinfo=tzn).date()
                final_date = (datetime.now(tz=tzn).date() - finding_date)
                finding['edad'] = ":n".replace(":n", str(final_date.days))
        return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error')
        return None

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_evidences(request):
    finding_id = request.GET.get('id', None)
    resp = integrates_dao.get_finding_dynamo(int(finding_id))
    return util.response(resp, 'Success', False)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def get_evidence(request, findingid, fileid):
    if fileid is None:
        rollbar.report_message('Error: Missing evidence image ID', 'error', request)
        return HttpResponse("Error - Unsent image ID", content_type="text/html")
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.png': '.tmp', '.gif': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            return retrieve_image(request, localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to evidence denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid evidence image ID format', 'error', request)
            return HttpResponse("Error - ID with wrong format", content_type="text/html")
        drive_api = DriveAPI(fileid)
        # pylint: disable=W0622
        if not drive_api.FILE:
            rollbar.report_message('Error: Unable to download the evidence image', 'error', request)
            return HttpResponse("Error - Unable to download the image", content_type="text/html")
        else:
            filename = "/tmp/:id.tmp".replace(":id", fileid)
            return retrieve_image(request, filename)

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def retrieve_image(request, img_file):
    mime = Magic(mime=True)
    mime_type = mime.from_file(img_file)
    try:
        if mime_type.startswith('image/'):
            with open(img_file, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type=mime_type)
        else:
            rollbar.report_message('Error: Invalid evidence image format: ' + mime_type, 'error', request)
            return HttpResponse("Error: Invalid evidence image format", content_type="text/html")
    finally:
        os.unlink(img_file)

@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def update_evidences_files(request):
    parameters = request.POST.dict()
    if catch_finding(request,parameters['findingId']) is None:
        return util.response([], 'Access denied', True)
    upload = request.FILES.get("document", "")
    migrate_all_files(parameters, request)
    mime = Magic(mime=True)
    if isinstance(upload, TemporaryUploadedFile):
        mime_type = mime.from_file(upload.temporary_file_path())
    elif isinstance(upload, InMemoryUploadedFile):
        mime_type = mime.from_buffer(upload.file.getvalue())
    fieldNum = FindingDTO()
    fieldname = [['animation', fieldNum.ANIMATION], ['exploitation', fieldNum.EXPLOTATION], \
                ['evidence_route_1', fieldNum.DOC_ACHV1], ['evidence_route_2', fieldNum.DOC_ACHV2], \
                ['evidence_route_3', fieldNum.DOC_ACHV3], ['evidence_route_4', fieldNum.DOC_ACHV4], \
                ['evidence_route_5', fieldNum.DOC_ACHV5], ['exploit', fieldNum.EXPLOIT], \
                ['fileRecords', fieldNum.REG_FILE]]
    if mime_type == "image/gif" and parameters["id"] == '0':
        if upload.size > 10485760:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "image/png" and parameters["id"] == '1':
        if upload.size > 2097152:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "image/png" and parameters["id"] in ['2', '3', '4', '5', '6']:
        if upload.size > 2097152:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif (mime_type == "text/x-python" or mime_type == "text/x-c" \
                or mime_type == "text/plain" or mime_type == "text/html") \
                    and parameters["id"] == '7':
        if upload.size > 1048576:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'File exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "text/plain" and parameters["id"] == '8':
        if upload.size > 1048576:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'File exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    rollbar.report_message('Error - Extension not allowed', 'error', request)
    return util.response([], 'Extension not allowed', True)

def key_existing_list(key):
    """return the key's list if it exist, else list empty"""
    response = client_s3.list_objects_v2(
        Bucket=bucket_s3,
        Prefix=key,
    )
    key_list = []
    for obj in response.get('Contents', []):
        key_list.append(obj['Key'])
    return key_list

def send_file_to_s3(filename, parameters, field, fieldname, ext):
    fileurl = parameters['findingId'] + '/' + parameters['url']
    fileroute = "/tmp/:id.tmp".replace(":id", filename)
    namecomplete = fileurl + "-" + field + "-" + filename + ext
    if os.path.exists(fileroute):
        with open(fileroute, "r") as file_obj:
            try:
                client_s3.upload_fileobj(file_obj, bucket_s3, namecomplete)
            except ClientError:
                rollbar.report_exc_info()
                integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
                return False
        resp = integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, True)
        if not resp:
            integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
        os.unlink(fileroute)
        return resp
    else:
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
        return False

def update_file_to_s3(parameters, field, fieldname, upload):
    fileurl = parameters['findingId'] + '/' + parameters['url']
    key_val = fileurl + "-" + field
    key_list = key_existing_list(key_val)
    if key_list:
        for k in key_list:
            client_s3.delete_object(Bucket=bucket_s3, Key=k)
    filename = fileurl + "-" + field + "-" + upload.name
    try:
        client_s3.upload_fileobj(upload.file, bucket_s3, filename)
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, filename.split("/")[1], "is_" + fieldname, True)
        return False
    except ClientError:
        rollbar.report_exc_info()
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, filename.split("/")[1], "is_" + fieldname, False)
        return True

def migrate_all_files(parameters, request):
    fin_dto = FindingDTO()
    try:
        api = FormstackAPI()
        frmreq = api.get_submission(parameters['findingId'])
        finding = fin_dto.parse(parameters['findingId'], frmreq, request)
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.ANIMATION
        folder = key_existing_list(filename)
        if "animation" in finding and parameters["id"] != '0' and not folder:
            send_file_to_s3(finding["animation"], parameters, fin_dto.ANIMATION, "animation", ".gif")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOTATION
        folder = key_existing_list(filename)
        if "exploitation" in finding and parameters["id"] != '1' and not folder:
            send_file_to_s3(finding["exploitation"], parameters, fin_dto.EXPLOTATION, "exploitation", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV1
        folder = key_existing_list(filename)
        if "evidence_route_1" in finding and parameters["id"] != '2' and not folder:
            send_file_to_s3(finding["evidence_route_1"], parameters, fin_dto.DOC_ACHV1, "evidence_route_1", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV2
        folder = key_existing_list(filename)
        if "evidence_route_2" in finding and parameters["id"] != '3' and not folder:
            send_file_to_s3(finding["evidence_route_2"], parameters, fin_dto.DOC_ACHV2, "evidence_route_2", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV3
        folder = key_existing_list(filename)
        if "evidence_route_3" in finding and parameters["id"] != '4' and not folder:
            send_file_to_s3(finding["evidence_route_3"], parameters, fin_dto.DOC_ACHV3, "evidence_route_3", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV4
        folder = key_existing_list(filename)
        if "evidence_route_4" in finding and parameters["id"] != '5' and not folder:
            send_file_to_s3(finding["evidence_route_4"], parameters, fin_dto.DOC_ACHV4, "evidence_route_4", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV5
        folder = key_existing_list(filename)
        if "evidence_route_5" in finding and parameters["id"] != '6' and not folder:
            send_file_to_s3(finding["evidence_route_5"], parameters, fin_dto.DOC_ACHV5, "evidence_route_5", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOIT
        folder = key_existing_list(filename)
        if "exploit" in finding and parameters["id"] != '7' and not folder:
            send_file_to_s3(finding["exploit"], parameters, fin_dto.EXPLOIT, "exploit", ".py")
        filename = parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.REG_FILE
        folder = key_existing_list(filename)
        if "fileRecords" in finding and parameters["id"] != '8' and not folder:
            send_file_to_s3(finding["fileRecords"], parameters, fin_dto.REG_FILE, "fileRecords", ".csv")
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def update_evidence_text(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_evidence_description(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating evidence description', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_exploit(request):
    parameters = request.GET.dict()
    fileid = parameters['id']
    findingid = parameters['findingid']
    if fileid is None:
        rollbar.report_message('Error: Missing exploit ID', 'error', request)
        return HttpResponse("Error - Unsent exploit ID", content_type="text/html")
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.py': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            mime = Magic(mime=True)
            mime_type = mime.from_file(localtmp)
            if mime_type == "text/x-python" or mime_type == "text/x-c" \
                or mime_type == "text/plain" or mime_type == "text/html":
                with open(localtmp, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="text/plain")
            os.unlink(localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to exploit denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid exploit ID format', 'error', request)
            return HttpResponse("Error - ID with wrong format", content_type="text/html")
        drive_api = DriveAPI(fileid)
        if drive_api.FILE is None:
            rollbar.report_message('Error: Unable to download the exploit', 'error', request)
            return HttpResponse("Error - Unable to download the file", content_type="text/html")
        filename = "/tmp/:id.tmp".replace(":id", fileid)
        mime = Magic(mime=True)
        mime_type = mime.from_file(filename)
        if mime_type == "text/x-c" or mime_type == "text/x-python" or mime_type == "text/plain" \
            or mime_type == "text/html":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="text/plain")
        os.unlink(filename)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_records(request):
    parameters = request.GET.dict()
    fileid = parameters['id']
    findingid = parameters['findingid']
    if fileid is None:
        rollbar.report_message('Error: Missing record file ID', 'error', request)
        return util.response([], 'Unsent record file ID', True)
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.py': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            return retrieve_csv(request, localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to record file denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid record file ID format', 'error', request)
            return util.response([], 'ID with wrong format', True)
        drive_api = DriveAPI(fileid)
        if drive_api.FILE is None:
            rollbar.report_message('Error: Unable to download the record file', 'error', request)
            return util.response([], 'Unable to download the file', True)
        filename = "/tmp/:id.tmp".replace(":id", fileid)
        return retrieve_csv(request, filename)

def retrieve_csv(request, csv_file):
    mime = Magic(mime=True)
    mime_type = mime.from_file(csv_file)
    data = []
    try:
        if mime_type == "text/plain":
            with io.open(csv_file, 'r', encoding='utf-8', errors='ignore') as file_obj:
                csvReader = csv.reader(x.replace('\0', '') for x in file_obj)
                header = csvReader.next()
                for row in csvReader:
                    dicTok = list_to_dict(header, row)
                    data.append(dicTok)
                return util.response(data, 'Success', False)
        else:
            rollbar.report_message('Error: Invalid record file format: ' + mime_type, 'error', request)
            return util.response([], 'Invalid record file format', True)
    finally:
        os.unlink(csv_file)

def list_to_dict(header, li):
    dct = {}
    cont = 0
    if len(header) < len(li):
        dif  = len(li) - len(header)
        for x in range(dif): # pylint: disable=unused-variable
            header.append("")
    elif len(header) > len(li):
        dif  = len(header) - len(li)
        for x in range(dif): # pylint: disable=unused-variable
            li.append("")

    for item in li:
        if header[cont] == "":
            dct[cont] = item
        else:
            dct[header[cont]] = item
        cont += 1
    return dct

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_myevents(request):
    user = request.session["username"]
    projects = integrates_dao.get_projects_by_user(user)
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    for row in projects:
        project = row[0]
        submissions = api.get_eventualities(project)
        if not submissions is None and 'error' not in submissions:
            frmset = submissions["submissions"]
            for evtsub in frmset:
                submission = api.get_submission(evtsub["id"])
                if not "error" in submission:
                    evtset = evt_dto.parse(evtsub["id"], submission)
                    if evtset['fluidProject'].lower() == project.lower():
                        if evtset['estado'] == "Pendiente":
                            dataset.append(evtset)
    return util.response(dataset, 'Success', False)


@never_cache
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
def update_cssv2(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_cssv2(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating CSSV2', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def update_description(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_description(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating description', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
def update_treatment(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_treatment(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating treatment', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def update_eventuality(request):
    "Update an eventuality associated to a project"
    parameters = request.POST.dict()
    try:
        generic_dto = EventualityDTO()
        generic_dto.create(parameters)
        if not parameters["vuln[affectation]"].isdigit():
            rollbar.report_message('Error: Affectation can not be a negative number', 'error', request)
            return util.response([], 'Afectacion negativa', True)
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error ocurred updating event', 'error', request)
        return util.response([], 'error', True)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def delete_finding(request):
    """Capture and process the ID of an eventuality to eliminate it"""
    parameters = request.POST.dict()
    username = request.session['username']
    if catch_finding(request,parameters["data[id]"]) is None:
        return util.response([], 'Access denied', True)
    fin_dto = FindingDTO()
    try:
        submission_id = parameters["data[id]"]
        context = fin_dto.create_delete(parameters, username, "", "")
        api = FormstackAPI()
        frmreq = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmreq, request)
        context["project"] = finding["fluidProject"]
        context["name_finding"] = finding["finding"]
        result = api.delete_submission(submission_id)
        if result is None:
            rollbar.report_message('Error: An error ocurred deleting finding', 'error', request)
            return util.response([], 'Error', True)
        to = ["engineering@fluidattacks.com"]
        send_mail_delete_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
def finding_solved(request):
    """ Send an email requesting the verification of a finding """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    remediated = integrates_dao.add_remediated_dynamo(
        int(parameters['data[findingId]']),
        True,
        parameters['data[project]'],
        parameters['data[findingName]'])
    rem_solution = parameters['data[justification]'].replace('\n', ' ')
    if not remediated:
        rollbar.report_message('Error: An error occurred when remediating the finding', 'error', request)
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
           'finding_id': parameters['data[findingId]'],
           'finding_vulns': parameters['data[findingVulns]'],
           'company': request.session["company"],
           'solution': rem_solution,
            }
        send_mail_remediate_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def finding_verified(request):
    """ Send an email notifying that the finding was verified """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    verified = integrates_dao.add_remediated_dynamo(
        int(parameters['data[findingId]']),
        False, parameters['data[project]'],
        parameters['data[findingName]'])
    if not verified:
        rollbar.report_message('Error: An error occurred when verifying the finding', 'error', request)
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
           'finding_id': parameters['data[findingId]'],
           'finding_vulns': parameters['data[findingVulns]'],
           'company': request.session["company"],
            }
        send_mail_verified_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_remediated(request):
    finding_id = request.GET.get('id', "")
    remediated = integrates_dao.get_remediated_dynamo(int(finding_id))
    if remediated == []:
        return util.response({'remediated': False}, 'Success', False)
    resp = False
    for row in remediated:
        resp = row['remediated']
    return util.response({'remediated': resp}, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_comments(request):
    submission_id = request.GET.get('id', "")
    comments = integrates_dao.get_comments_dynamo(int(submission_id))
    json_data = []
    for row in comments:
        aux = row['email'] == request.session["username"]
        json_data.append({
            'id': int(row['user_id']),
            'parent': int(row['parent']),
            'created': row['created'],
            'modified': row['modified'],
            'content': row['content'],
            'fullname': row['fullname'],
            'created_by_current_user': aux,
            'email': row['email']
        })
    return util.response(json_data, 'Success', False)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
def add_comment(request):
    submission_id = request.POST.get('id', "")
    data = request.POST.dict()
    data["data[created]"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["data[modified]"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    email = request.session["username"]
    data["data[fullname]"] = request.session["first_name"] + " " + request.session["last_name"]
    comment = integrates_dao.create_comment_dynamo(int(submission_id), email, data)
    if not comment:
        rollbar.report_message('Error: An error ocurred adding comment', 'error', request)
        return util.response([], 'Error', True)
    try:
        recipients = integrates_dao.get_project_users(data['data[project]'].lower())
        to = [x[0] for x in recipients if x[1] == 1]
        to.append('continuous@fluidattacks.com')
        comment_content = data['data[content]'].replace('\n', ' ')
        context = {
           'project': data['data[project]'],
           'finding_name': data['data[findingName]'],
           'user_email': email,
           'finding_url': data['data[findingUrl]'],
           'finding_id': submission_id,
           'comment': comment_content,
            }
        if data["data[remediated]"] != "true":
            if data["data[parent]"] == '0':
                send_mail_new_comment(to, context)
                return util.response([], 'Success', False)
            elif data["data[parent]"] != '0':
                send_mail_reply_comment(to, context)
                return util.response([], 'Success', False)
        else:
            return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
def delete_comment(request):
    submission_id = request.POST.get('id', "")
    data = request.POST.dict()
    comment = integrates_dao.delete_comment_dynamo(int(submission_id), data)
    if not comment:
        rollbar.report_message('Error: An error ocurred deleting comment', 'error', request)
        return util.response([], 'Error', True)
    return util.response([], 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def total_severity(request):
    project = request.GET.get('project', "")
    toe = integrates_dao.get_toe_dynamo(project)
    return util.response(toe, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def get_alerts(request):
    company = request.GET.get('company', None)
    project = request.GET.get('project', None)
    resp = integrates_dao.get_company_alert_dynamo(company, project)
    return util.response(resp, 'Success', False)

@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
# pylint: disable=R0101
def accept_release(request):
    parameters = request.POST.get('id', "")
    generic_dto = FindingDTO()
    try:
        finding = catch_finding(request, parameters)
        if "releaseDate" not in finding:
            tzn = pytz.timezone('America/Bogota')
            releaseDate = datetime.now(tz=tzn).date()
            if ("suscripcion" in finding and
                (finding["suscripcion"] == "Continua" or
                    finding["suscripcion"] == "Concurrente" or
                    finding["suscripcion"] == "Si")):
                releases = integrates_dao.get_project_dynamo(finding["fluidProject"].lower())
                for release in releases:
                    if "lastRelease" in release:
                        last_release = datetime.strptime(
                            release["lastRelease"].split(" ")[0],
                            '%Y-%m-%d'
                        )
                        last_release = last_release.replace(tzinfo=tzn).date()
                        if last_release == releaseDate:
                            releaseDate = releaseDate + timedelta(days=1)
                        elif last_release > releaseDate:
                            releaseDate = last_release + timedelta(days=1)
            releaseDate = releaseDate.strftime('%Y-%m-%d %H:%M:%S')
            release = {}
            release['id'] = parameters
            release['releaseDate'] = releaseDate
            generic_dto.create_release(release)
            generic_dto.to_formstack()
            api = FormstackAPI()
            request = api.update(generic_dto.request_id, generic_dto.data)
            if request:
                integrates_dao.add_release_toproject_dynamo(finding["fluidProject"], True, releaseDate)
                return util.response([], 'success', False)
            rollbar.report_message('Error: An error occurred accepting the release', 'error', request)
            return util.response([], 'error', True)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
def reject_release(request):
    parameters = request.POST.dict()
    username = request.session['username']
    fin_dto = FindingDTO()
    try:
        submission_id = parameters["data[id]"]
        findingData = catch_finding(request, submission_id)
        if "releaseDate" not in findingData:
            api = FormstackAPI()
            frmreq = api.get_submission(submission_id)
            finding = fin_dto.parse(submission_id, frmreq, request)
            context = {
               'project': finding['fluidProject'],
               'analyst_mail': finding['analyst'],
               'finding_name': finding['finding'],
               'admin_mail': username,
               'finding_id': submission_id,
               'rejectionCause': parameters['data[justification]'],
            }
            result = api.delete_submission(submission_id)
            if result is None:
                rollbar.report_message('Error: An error ocurred deleting the release', 'error', request)
                return util.response([], 'Error', True)
            to = ["jrestrepo@fluidattacks.com", "ralvarez@fluidattacks.com",
                  "aroldan@fluidattacks.com", finding['analyst']]
            send_mail_reject_release(to, context)
            return util.response([], 'success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_project_access
def add_access_integrates(request):
    parameters = request.POST.dict()
    newUser = parameters['data[userEmail]']
    company = parameters['data[company]']
    admin = parameters['data[admin]']
    role = parameters['data[userRole]']
    project = request.POST.get('project', '')

    if (request.session['role'] == 'admin'):
        if (role == 'admin' or role == 'analyst' or
                role == 'customer'or role == 'customeradmin'):
            if create_new_user(newUser, role, company, project, admin):
                return util.response([], 'Success', False)
            else:
                rollbar.report_message("Error: Couldn't grant access to project", 'error', request)
                return util.response([], 'Error', True)
        else:
            rollbar.report_message('Error: Invalid role provided: ' + role, 'error', request)
            return util.response([], 'Error', True)
    elif is_customeradmin(project, request.session['username']):
        if (role == 'customer' or role == 'customeradmin'):
            if create_new_user(newUser, role, company, project, admin):
                return util.response([], 'Success', False)
            else:
                rollbar.report_message("Error: Couldn't grant access to project", 'error', request)
                return util.response([], 'Error', True)
        else:
            rollbar.report_message('Error: Invalid role provided: ' + role, 'error', request)
            return util.response([], 'Error', True)
    else:
        rollbar.report_message('Error: Only admin / customeradmin roles are allowed to add users', 'error', request)
        return util.response([], 'Access denied', True)

def create_new_user(newUser, role, company, project, admin):
    project_url = 'https://fluidattacks.com/integrates/dashboard#!/project/' \
                  + project.lower() + '/indicators'
    if not integrates_dao.is_in_database(newUser):
        integrates_dao.create_user_dao(newUser)
    if integrates_dao.is_registered_dao(newUser) == '0':
        integrates_dao.register(newUser)
        integrates_dao.assign_role(newUser, role)
        integrates_dao.assign_company(newUser, company)
    elif integrates_dao.is_registered_dao(newUser) == '1':
        integrates_dao.assign_role(newUser, role)
    if role == 'customeradmin':
        integrates_dao.add_role_to_project_dynamo(project.lower(), newUser, role)
    if integrates_dao.add_access_to_project_dao(newUser, project):
        description = integrates_dao.get_project_description(project)
        to = [newUser]
        context = {
           'admin': admin,
           'project': project,
           'project_description': description,
           'project_url': project_url,
        }
        send_mail_access_granted(to, context)
        return True
    else:
        return False

def calculate_indicators(project):
    api = FormstackAPI()
    evt_dto = EventualityDTO()
    openVulnerabilities = cardinalidadTotal = maximumSeverity = openEvents =  0
    for row in  api.get_eventualities(project)["submissions"]:
        evtset = evt_dto.parse(row["id"], api.get_submission(row["id"]))
        if evtset['estado']=='Pendiente':
            openEvents += 1
    for finding in api.get_findings(project)["submissions"]:
        act_finding = finding_vulnerabilities(str(finding['id']))
        openVulnerabilities += int(act_finding['openVulnerabilities'])
        cardinalidadTotal += int(act_finding['cardinalidad_total'])
        if (maximumSeverity < float(act_finding['criticity'])):
            maximumSeverity = float(act_finding['criticity'])
    try:
        fixed_vuln = int(round((1.0 - (float(openVulnerabilities) / float(cardinalidadTotal)))*100.0))
    except ZeroDivisionError:
        fixed_vuln = 0
    return [openEvents,maximumSeverity, fixed_vuln]

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

@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_project_access
def remove_access_integrates(request):
    parameters = request.POST.dict()
    user = parameters['email']
    project = parameters['project']
    if (is_customeradmin(project, request.session['username']) or
            request.session['role'] == 'admin'):
        if integrates_dao.remove_access_project_dao(user, project):
            if is_customeradmin(project, user):
                integrates_dao.remove_role_to_project_dynamo(project, user, "customeradmin")
            return util.response([], 'Success', False)
    return util.response([], 'Error', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_project_access
def change_user_role(request):
    email = request.POST.get('email', "")
    role = request.POST.get('role', "")
    project = request.POST.get('project', "")
    if request.session['role'] == 'admin':
        if (role == 'admin' or role == 'analyst' or
                role == 'customer'or role == 'customeradmin'):
            if integrates_dao.assign_role(email, role) is None:
                if role == 'customeradmin':
                    integrates_dao.add_role_to_project_dynamo(project.lower(), email, role)
                elif is_customeradmin(project, email):
                    integrates_dao.remove_role_to_project_dynamo(project, email, "customeradmin")
                return util.response([], 'Success', False)
    elif is_customeradmin(project, request.session['username']):
        if role == 'customer'or role == 'customeradmin':
            if integrates_dao.assign_role(email, role) is None:
                if role == 'customeradmin':
                    integrates_dao.add_role_to_project_dynamo(project.lower(), email, role)
                elif is_customeradmin(project, email):
                    integrates_dao.remove_role_to_project_dynamo(project, email, "customeradmin")
                return util.response([], 'Success', False)
    return util.response([], 'Error', True)

@never_cache
@require_http_methods(["POST"])
@authenticate
def legal_status(request):
    status = request.POST.get('status', "")
    request.session['legal_status'] = status
    return util.response([], 'Success', False)

@never_cache
@require_http_methods(["GET"])
@authenticate
def is_registered(request):
    user = request.session['username'];
    return util.response([], integrates_dao.is_registered_dao(user), False)

@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
def graphql_api(request):
    query = request.body
    schema = Schema(query=Query)
    result = schema.execute(query)
    return util.response(result.data, 'success', False)

@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def access_to_project(request):
    project = request.GET.get('project', "")
    if has_access_to_project(request.session['username'], project, request.session['role']):
        return util.response(True, 'success', False)
    return util.response(False, 'success', False)
