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
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize, require_project_access, require_finding_access
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
from .mailer import send_mail_delete_draft
from .mailer import send_mail_access_granted
from .mailer import send_mail_repositories
from .services import has_access_to_project, has_access_to_finding
from .services import is_customeradmin, has_responsibility, has_phone_number
from .dao import integrates_dao
from .api.drive import DriveAPI
from .api.formstack import FormstackAPI
from magic import Magic
from datetime import datetime, timedelta
from backports import csv
from .entity.query import Query
from .entity.mutations import Mutations
from graphene import Schema
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET

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
               "delete_project": "Delete Project",
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
                   "delete_project": "Borrar Proyecto",
                   "documentation": "Documentacion"
                }
            }
        }
    return render(request, "project/findings.html", dicLang)

@never_cache
@authenticate
@authorize(['analyst', 'admin'])
def project_drafts(request):
    "Drafts view"
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
    return render(request, "project/drafts.html", dicLang)

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
def project_resources(request):
    "resources view"
    language = request.GET.get('l', 'en')
    dicLang = {
        "search_findings": {
            "environment_table": {
                "environment": "Environment"
            },
            "repositories_table": {
                "branch": "Branch",
                "repository": "Repository"
            },
        }
    }
    if language == "es":
        dicLang = {
            "search_findings": {
                "environment_table": {
                    "environment": "Ambiente"
                },
                "repositories_table": {
                    "branch": "Rama",
                    "repository": "Repositorio"
                },
            }
        }
    return render(request, "project/resources.html", dicLang)

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
               "phoneNumber": "Phone Number",
               "userResponsibility": "Responsibility",
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
                   "phoneNumber": "Número Telefónico",
                   "userResponsibility": "Responsabilidad",
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
        util.cloudwatch_log(request, 'Security: Attempted to export project xls without permission')
        return util.response([], 'Access denied', True)
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    for reqset in FormstackAPI().get_findings(project)["submissions"]:
        fin = catch_finding(request, reqset["id"])
        if fin['fluidProject'].lower() == project.lower() and \
                util.validate_release_date(fin):
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
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(request.session['username'], project, request.session['role']):
        util.cloudwatch_log(request, 'Security: Attempted to export project pdf without permission')
        return util.response([], 'Access denied', True)
    else:
        user = request.session['username'].split("@")[0]
        validator = validation_project_to_pdf(request, lang, doctype)
        if validator is not None:
            return validator
        for reqset in FormstackAPI().get_findings(project)["submissions"]:
            fin = catch_finding(request, reqset["id"])
            if fin['fluidProject'].lower() == project.lower() and \
                    util.validate_release_date(fin):
                findings.append(fin)
        pdf_maker = CreatorPDF(lang, doctype)
        secure_pdf = SecurePDF()
        findings_ord = util.ord_asc_by_criticidad(findings)
        findings = pdf_evidences(findings_ord)
        report_filename = ""
        if doctype == "tech":
            pdf_maker.tech(findings, project, user)
            report_filename = secure_pdf.create_full(user, pdf_maker.out_name)
        elif doctype == "executive":
            return HttpResponse("Disabled report generation", content_type="text/html")
        else:
            report_filename = presentation_pdf(project, pdf_maker, findings, user)
            if report_filename == "Incorrect parametrization":
                return HttpResponse("Incorrect parametrization", content_type="text/html")
            elif report_filename == "Incomplete documentation":
                return HttpResponse("Incomplete documentation", content_type="text/html")
        if not os.path.isfile(report_filename):
            rollbar.report_message('Error: Documentation has not been generated', 'error', request)
            raise HttpResponse('Documentation has not been generated :(', content_type="text/html")
        with open(report_filename, 'r') as document:
            response = HttpResponse(document.read(),
                                    content_type="application/pdf")
            response['Content-Disposition'] = \
                "inline;filename=:id.pdf".replace(":id", user + "_" + project)
        return response

def pdf_evidences(findings):
    fin_dto = FindingDTO()
    for finding in findings:
        key_list = key_existing_list(finding['id'])
        field_list = [fin_dto.DOC_ACHV1, fin_dto.DOC_ACHV2, \
                    fin_dto.DOC_ACHV3, fin_dto.DOC_ACHV4, \
                    fin_dto.DOC_ACHV5]
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
    return findings

def presentation_pdf(project, pdf_maker, findings, user):
    project_info = get_project_info(project)
    mapa_id = util.drive_url_filter(project_info["findingsMap"])
    project_info["findingsMap"] = "image::../images/"+mapa_id+'.png[align="center"]'
    DriveAPI().download_images(mapa_id)
    nivel_sec = project_info["securityLevel"].split(" ")[0]
    if not util.is_numeric(nivel_sec):
        return "Incorrect parametrization"
    nivel_sec = int(nivel_sec)
    if nivel_sec < 0 or nivel_sec > 6:
        return "Incorrect parametrization"
    project_info["securityLevel"] = "image::../resources/presentation_theme/nivelsec"+str(nivel_sec)+'.png[align="center"]'
    if not project_info:
        return "Incomplete documentation"
    pdf_maker.presentation(findings, project, project_info, user)
    #secure_pdf = SecurePDF()
    #report_filename = secure_pdf.create_only_pass(user, pdf_maker.out_name)
    report_filename = pdf_maker.RESULT_DIR + pdf_maker.out_name
    return report_filename

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
        util.cloudwatch_log(request, 'Security: Attempted to export project pdf without permission')
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
            rollbar.report_message('Error: Formstack returned an error getting events', 'error', request)
            return util.response(dataset, 'An error occurred getting events', True)
    elif category == "ID":
        # Only fluid can filter by id
        if "@fluidattacks.com" not in username:
            util.cloudwatch_log(request, 'Security: Non-fluid user attempted to filter events by ID')
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
            rollbar.report_message('Error: Formstack returned an error getting events', 'error', request)
            return util.response(dataset, 'An error occurred getting events', True)
    else:
        util.cloudwatch_log(request, 'Security: Attempted to get eventualities by unknown filter: ' + category)
        return util.response(dataset, 'Unknown filter', True)

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
        util.cloudwatch_log(request, 'Security: Attempted to retrieve project users without permission')
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
        user_responsibility = has_responsibility(project, user)
        user_phone = has_phone_number(user)
        data['userResponsibility'] = user_responsibility
        if is_customeradmin(project, user):
            data['userRole'] = "customer_admin"
        elif userRole == "customeradmin":
            data['userRole'] = "customer"
        else:
            data['userRole'] = userRole
        data["userPhone"] = user_phone
        dataset.append(data)
    return util.response(dataset, 'Success', False)

@cache_control(max_age=600)
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_finding_access
def get_finding(request):
    submission_id = request.POST.get('findingid', "")
    finding = catch_finding(request, submission_id)
    if finding is not None:
        if finding['vulnerability'].lower() == 'masked':
            util.cloudwatch_log(request, 'Warning: Project masked')
            return util.response([], 'Project masked', True)
        else:
            return util.response(finding, 'Success', False)
    else:
        util.cloudwatch_log(request, 'Finding with submission id: ' + submission_id + ' not found')
        return util.response([], 'Error', True)

@never_cache
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
        if finding['fluidProject'].lower() == project.lower() and \
                'releaseDate' not in finding:
            findings.append(finding)
    return util.response(findings, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_findings(request):
    """Capture and process the name of a project to return the findings."""
    project = request.GET.get('project', "").encode('utf-8')
    project = project.lower()
    if util.validate_session_time(project, request):
        return util.response(request.session["projects"][project], 'Success', False)
    else:
        api = FormstackAPI()
        findings = []
        finreqset = api.get_findings(project)["submissions"]
        for submission_id in finreqset:
            finding = catch_finding(request, submission_id["id"])
            if finding is not None:
                if finding['vulnerability'].lower() == 'masked':
                    util.cloudwatch_log(request, 'Warning: Project masked')
                    return util.response([], 'Project masked', True)
                elif finding['fluidProject'].lower() == project and \
                        util.validate_release_date(finding):
                    findings.append(finding)
            else:
                rollbar.report_message('Error: An error occurred catching finding', 'error', request)
        request.session["projects"][project] = findings
        request.session["projects"][project + "_date"] = str(datetime.today())
        return util.response(request.session["projects"][project], 'Success', False)

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
@require_finding_access
def get_evidences(request):
    finding_id = request.GET.get('findingid', None)
    resp = integrates_dao.get_finding_dynamo(int(finding_id))
    return util.response(resp, 'Success', False)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer', 'admin'])
def get_evidence(request, findingid, fileid):
    if not has_access_to_finding(request.session['access'], findingid, request.session['role']):
        util.cloudwatch_log(request, 'Security: Attempted to retrieve evidence img without permission')
        return util.response([], 'Access denied', True)
    else:
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
            if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
                rollbar.report_message('Error: Invalid evidence image ID format', 'error', request)
                return HttpResponse("Error - ID with wrong format", content_type="text/html")
            else:
                drive_api = DriveAPI()
                evidence_img = drive_api.download(fileid)
                return retrieve_image(request, evidence_img)

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def retrieve_image(request, img_file):
    try:
        if util.assert_file_mime(img_file, ["image/png", "image/jpeg", "image/gif"]):
            with open(img_file, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="image/*")
        else:
            rollbar.report_message('Error: Invalid evidence image format', 'error', request)
            return HttpResponse("Error: Invalid evidence image format", content_type="text/html")
    finally:
        if os.path.exists(img_file):
            os.unlink(img_file)

@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
def update_evidences_files(request):
    parameters = request.POST.dict()
    if not has_access_to_finding(request.session['access'], parameters['findingid'], request.session['role']):
        util.cloudwatch_log(request, 'Security: Attempted to update evidence img without permission')
        return util.response([], 'Access denied', True)
    else:
        if catch_finding(request,parameters['findingid']) is None:
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

        if mime_type not in ["image/gif", "image/png", "text/x-python",
                             "text/x-c", "text/plain", "text/html"]:
            # Handle a possible front-end validation bypass
            util.cloudwatch_log(request, 'Security: Attempted to upload evidence file with a non-allowed format: ' + mime_type)
            return util.response([], 'Extension not allowed', True)
        else:
            if evidence_exceeds_size(upload, mime_type, int(parameters["id"])):
                rollbar.report_message('Error - File exceeds the size limits', 'error', request)
                return util.response([], 'File exceeds the size limits', True)
            else:
                updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
                return util.response([], 'sent', updated)

def evidence_exceeds_size(uploaded_file, mime_type, evidence_type):
    ANIMATION = 0
    EXPLOITATION = 1
    EVIDENCE = [2, 3, 4, 5, 6]
    EXPLOIT = 7
    RECORDS = 8
    MIB = 1048576

    if evidence_type == ANIMATION and mime_type == "image/gif":
        return uploaded_file.size > 10 * MIB
    elif evidence_type == EXPLOITATION and mime_type == "image/png":
        return uploaded_file.size > 2 * MIB
    elif evidence_type in EVIDENCE and mime_type == "image/png":
        return uploaded_file.size > 2 * MIB
    elif evidence_type == EXPLOIT and mime_type in ["text/html", "text/plain",
                                                    "text/x-c", "text/x-python"]:
        return uploaded_file.size > 1 * MIB
    elif evidence_type == RECORDS and mime_type == "text/plain":
        return uploaded_file.size > 1 * MIB
    else:
        return False

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
    fileurl = parameters['findingid'] + '/' + parameters['url']
    fileroute = "/tmp/:id.tmp".replace(":id", filename)
    namecomplete = fileurl + "-" + field + "-" + filename + ext
    if os.path.exists(fileroute):
        with open(fileroute, "r") as file_obj:
            try:
                client_s3.upload_fileobj(file_obj, bucket_s3, namecomplete)
            except ClientError:
                rollbar.report_exc_info()
                integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
                return False
        resp = integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, True)
        if not resp:
            integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
        os.unlink(fileroute)
        return resp
    else:
        integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, namecomplete.split("/")[1], "is_" + fieldname, False)
        return False

def update_file_to_s3(parameters, field, fieldname, upload):
    fileurl = parameters['findingid'] + '/' + parameters['url']
    key_val = fileurl + "-" + field
    key_list = key_existing_list(key_val)
    if key_list:
        for k in key_list:
            client_s3.delete_object(Bucket=bucket_s3, Key=k)
    filename = fileurl + "-" + field + "-" + upload.name
    try:
        client_s3.upload_fileobj(upload.file, bucket_s3, filename)
        integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, filename.split("/")[1], "is_" + fieldname, True)
        return False
    except ClientError:
        rollbar.report_exc_info()
        integrates_dao.add_finding_dynamo(int(parameters['findingid']), fieldname, filename.split("/")[1], "is_" + fieldname, False)
        return True

def migrate_all_files(parameters, request):
    fin_dto = FindingDTO()
    try:
        api = FormstackAPI()
        frmreq = api.get_submission(parameters['findingid'])
        finding = fin_dto.parse(parameters['findingid'], frmreq, request)
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.ANIMATION
        folder = key_existing_list(filename)
        if "animation" in finding and parameters["id"] != '0' and not folder:
            send_file_to_s3(finding["animation"], parameters, fin_dto.ANIMATION, "animation", ".gif")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOTATION
        folder = key_existing_list(filename)
        if "exploitation" in finding and parameters["id"] != '1' and not folder:
            send_file_to_s3(finding["exploitation"], parameters, fin_dto.EXPLOTATION, "exploitation", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV1
        folder = key_existing_list(filename)
        if "evidence_route_1" in finding and parameters["id"] != '2' and not folder:
            send_file_to_s3(finding["evidence_route_1"], parameters, fin_dto.DOC_ACHV1, "evidence_route_1", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV2
        folder = key_existing_list(filename)
        if "evidence_route_2" in finding and parameters["id"] != '3' and not folder:
            send_file_to_s3(finding["evidence_route_2"], parameters, fin_dto.DOC_ACHV2, "evidence_route_2", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV3
        folder = key_existing_list(filename)
        if "evidence_route_3" in finding and parameters["id"] != '4' and not folder:
            send_file_to_s3(finding["evidence_route_3"], parameters, fin_dto.DOC_ACHV3, "evidence_route_3", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV4
        folder = key_existing_list(filename)
        if "evidence_route_4" in finding and parameters["id"] != '5' and not folder:
            send_file_to_s3(finding["evidence_route_4"], parameters, fin_dto.DOC_ACHV4, "evidence_route_4", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV5
        folder = key_existing_list(filename)
        if "evidence_route_5" in finding and parameters["id"] != '6' and not folder:
            send_file_to_s3(finding["evidence_route_5"], parameters, fin_dto.DOC_ACHV5, "evidence_route_5", ".png")
        filename =  parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOIT
        folder = key_existing_list(filename)
        if "exploit" in finding and parameters["id"] != '7' and not folder:
            send_file_to_s3(finding["exploit"], parameters, fin_dto.EXPLOIT, "exploit", ".py")
        filename = parameters['findingid'] + "/" + parameters['url'] + "-" + fin_dto.REG_FILE
        folder = key_existing_list(filename)
        if "fileRecords" in finding and parameters["id"] != '8' and not folder:
            send_file_to_s3(finding["fileRecords"], parameters, fin_dto.REG_FILE, "fileRecords", ".csv")
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'admin'])
@require_finding_access
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
@require_finding_access
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
            return retrieve_script(request, localtmp)
    else:
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid exploit ID format', 'error', request)
            return HttpResponse("Error - ID with wrong format", content_type="text/html")
        else:
            drive_api = DriveAPI()
            exploit = drive_api.download(fileid)
            return retrieve_script(request, exploit)

def retrieve_script(request, script_file):
    try:
        if util.assert_file_mime(script_file, ["text/x-python", "text/x-c",
                                               "text/plain", "text/html"]):
            with open(script_file, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="text/plain")
        else:
            rollbar.report_message('Error: Invalid exploit file format', 'error', request)
            return util.response([], 'Invalid exploit file format', True)
    finally:
        if os.path.exists(script_file):
            os.unlink(script_file)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_finding_access
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
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid record file ID format', 'error', request)
            return util.response([], 'ID with wrong format', True)
        else:
            drive_api = DriveAPI()
            record = drive_api.download(fileid)
            return retrieve_csv(request, record)

def retrieve_csv(request, csv_file):
    data = []
    try:
        if util.assert_file_mime(csv_file, ["text/plain"]):
            with io.open(csv_file, 'r', encoding='utf-8', errors='ignore') as file_obj:
                csvReader = csv.reader(x.replace('\0', '') for x in file_obj)
                header = csvReader.next()
                for row in csvReader:
                    dicTok = list_to_dict(header, row)
                    data.append(dicTok)
                return util.response(data, 'Success', False)
        else:
            rollbar.report_message('Error: Invalid record file format', 'error', request)
            return util.response([], 'Invalid record file format', True)
    finally:
        if os.path.exists(csv_file):
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
@require_finding_access
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
@require_finding_access
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
@require_finding_access
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
@require_finding_access
def delete_finding(request):
    """Capture and process the ID of an eventuality to eliminate it"""
    submission_id = request.POST.get('findingid', "")
    parameters = request.POST.dict()
    username = request.session['username']
    if catch_finding(request, submission_id) is None:
        return util.response([], 'Access denied', True)
    fin_dto = FindingDTO()
    try:
        context = fin_dto.create_delete(parameters, username, "", submission_id)
        api = FormstackAPI()
        frmreq = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmreq, request)
        context["project"] = finding["fluidProject"]
        context["name_finding"] = finding["finding"]
        result = api.delete_submission(submission_id)
        if result is None:
            rollbar.report_message('Error: An error ocurred deleting finding', 'error', request)
            return util.response([], 'Error', True)
        to = ["projects@fluidattacks.com", "production@fluidattacks.com",
              "jarmas@fluidattacks.com", "jaguirre@fluidattacks.com"]
        send_mail_delete_finding(to, context)
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
           'finding_id': submission_id,
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

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_finding_access
def get_comments(request):
    comment_type = request.GET.get('commentType', "")
    if comment_type != 'comment' and comment_type != 'observation':
        rollbar.report_message('Error: Bad parameters in request', 'error', request)
        return util.response([], 'Bad parameters in request', True)
    elif comment_type == 'observation' and request.session['role'] == 'customer':
        util.cloudwatch_log(request, 'Security: Attempted to post observation without permission')
        return util.response([], 'Access denied', True)
    else:
        submission_id = request.GET.get('findingid', "")
        comments = integrates_dao.get_comments_dynamo(int(submission_id), comment_type)
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
@require_finding_access
def add_comment(request):
    submission_id = request.POST.get('findingid', "")
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
        if data['data[commentType]'] == 'observation':
            admins = integrates_dao.get_admins()
            to = [x[0] for x in admins]
            for user in recipients:
                if integrates_dao.get_role_dao(user[0]) == 'analyst':
                    to.append(user[0])
        else:
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
                send_mail_new_comment(to, context, data['data[commentType]'])
                return util.response([], 'Success', False)
            elif data["data[parent]"] != '0':
                send_mail_reply_comment(to, context, data['data[commentType]'])
                return util.response([], 'Success', False)
        else:
            return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)


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
@require_project_access
def get_alerts(request):
    company = request.GET.get('company', None)
    project = request.GET.get('project', None)
    resp = integrates_dao.get_company_alert_dynamo(company, project)
    return util.response(resp, 'Success', False)

@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
@require_finding_access
# pylint: disable=R0101
def accept_draft(request):
    parameters = request.POST.get('findingid', "")
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
            else:
                rollbar.report_message('Error: An error occurred accepting the draft', 'error', request)
                return util.response([], 'error', True)
        else:
            util.cloudwatch_log(request, 'Security: Attempted to accept an already released finding')
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
    username = request.session['username']
    fin_dto = FindingDTO()
    try:
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
            }
            result = api.delete_submission(submission_id)
            if result is None:
                rollbar.report_message('Error: An error ocurred deleting the draft', 'error', request)
                return util.response([], 'Error', True)
            admins = integrates_dao.get_admins()
            to = [x[0] for x in admins]
            to.append(finding['analyst'])
            send_mail_delete_draft(to, context)
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
    role = parameters['data[userRole]']
    project = request.POST.get('project', '')

    if (request.session['role'] == 'admin'):
        if (role == 'admin' or role == 'analyst' or
                role == 'customer'or role == 'customeradmin'):
            if create_new_user(parameters, project, request):
                return util.response([], 'Success', False)
            else:
                rollbar.report_message("Error: Couldn't grant access to project", 'error', request)
                return util.response([], 'Error', True)
        else:
            rollbar.report_message('Error: Invalid role provided: ' + role, 'error', request)
            return util.response([], 'Error', True)
    elif is_customeradmin(project, request.session['username']):
        if (role == 'customer' or role == 'customeradmin'):
            if create_new_user(parameters, project, request):
                return util.response([], 'Success', False)
            else:
                rollbar.report_message("Error: Couldn't grant access to project", 'error', request)
                return util.response([], 'Error', True)
        else:
            rollbar.report_message('Error: Invalid role provided: ' + role, 'error', request)
            return util.response([], 'Error', True)
    else:
        util.cloudwatch_log(request, 'Security: Attempted to grant access to project from unprivileged role: ' + request.session['role'])
        return util.response([], 'Access denied', True)

def create_new_user(parameters, project, request):
    newUser = parameters['data[userEmail]']
    company = parameters['data[userOrganization]']
    responsibility = parameters['data[userResponsibility]']
    role = parameters['data[userRole]']
    phone = parameters['data[userPhone]']
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
    len_responsibility = len(responsibility)
    if 0 < len_responsibility <= 50:
        integrates_dao.add_project_access_dynamo(newUser, project, "responsibility", responsibility)
    else:
        util.cloudwatch_log(
            request,
            'Security: ' + request.session['username'] + 'Attempted to add ' +
            'responsibility to project ' + project + ' without validation'
        )
    if phone:
        phone_number = phone[1:]
        if phone_number.isdigit():
            integrates_dao.add_phone_to_user_dynamo(newUser, phone)
    if role == 'customeradmin':
        integrates_dao.add_user_to_project_dynamo(project.lower(), newUser, role)
    if integrates_dao.add_access_to_project_dao(newUser, project):
        description = integrates_dao.get_project_description(project)
        to = [newUser]
        context = {
           'admin': request.session["username"],
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
        is_user_removed = remove_user_access(project, user)
        if is_user_removed:
            return util.response([], 'Success', False)
    return util.response([], 'Error', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['customer', 'admin'])
@require_project_access
def edit_user(request):
    parameters = request.POST.dict()
    role = parameters['data[userRole]']
    email = parameters['data[userEmail]']
    project = request.POST.get('project', "")
    if request.session['role'] == 'admin':
        if (role == 'admin' or role == 'analyst' or
                role == 'customer'or role == 'customeradmin'):
            if integrates_dao.assign_role(email, role) is None:
                edit_user_information(parameters, project, request)
                return util.response([], 'Success', False)
            else:
                return util.response([], 'Error', True)
    elif is_customeradmin(project, request.session['username']):
        if role == 'customer'or role == 'customeradmin':
            if integrates_dao.assign_role(email, role) is None:
                edit_user_information(parameters, project, request)
                return util.response([], 'Success', False)
            else:
                return util.response([], 'Error', True)
    return util.response([], 'Error', True)

def edit_user_information(parameters, project, request):
    project = project.lower()
    role = parameters['data[userRole]']
    email = parameters['data[userEmail]']
    responsibility = parameters['data[userResponsibility]']
    phone = parameters['data[userPhone]']
    organization = parameters['data[userOrganization]']
    len_responsibility = len(responsibility)
    integrates_dao.assign_company(email, organization.lower())
    if 0 < len_responsibility <= 50:
        integrates_dao.add_project_access_dynamo(email, project, "responsibility", responsibility)
    else:
        util.cloudwatch_log(
            request,
            'Security: ' + request.session['username'] + 'Attempted to add ' +
            'responsibility to project ' + project + ' without validation'
        )
    if phone:
        phone_number = phone[1:]
        if phone_number.isdigit():
            integrates_dao.add_phone_to_user_dynamo(email, phone)
        else:
            util.cloudwatch_log(
                request,
                'Security: ' + request.session['username'] + 'Attempted to ' +
                'add phone to user without validation'
            )
    else:
        util.cloudwatch_log(
            request,
            'Security: ' + request.session['username'] + 'Attempted to ' +
            'add phone to user without validation'
        )
    if role == 'customeradmin':
        integrates_dao.add_user_to_project_dynamo(project, email, role)
    elif is_customeradmin(project, email):
        integrates_dao.remove_role_to_project_dynamo(project, email, "customeradmin")

@never_cache
@require_http_methods(["POST"])
@authenticate
def graphql_api(request):
    query = request.body
    schema = Schema(query=Query, mutation=Mutations)
    result = schema.execute(query, context_value=request)
    if result.errors:
        for error in result.errors:
            rollbar.report_message('GraphQL Error: ' + str(error), 'error', request)
    return util.response(result.data, 'success', False)

@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
def access_to_project(request):
    project = request.GET.get('project', "")
    if has_access_to_project(request.session['username'], project, request.session['role']):
        return util.response(True, 'success', False)
    return util.response(False, 'success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_repositories(request):
    """Get the repositories of a project."""
    project = request.GET.get('project', None)
    json_info = []
    project_info = integrates_dao.get_project_dynamo(project)
    for info in project_info:
        if "repositories" in info:
            json_info = info['repositories']
            break
        else:
            json_info = []
    return util.response(json_info, 'Success', False)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def add_repositories(request):
    """Add repositories to proyect."""
    parameters = request.POST.dict()
    project = request.POST.get('project', "")
    total_repositories = parameters["data[totalRepo]"]
    json_data = []
    email_data = []
    for repo in range(int(total_repositories)):
        repository = 'data[repositories][{repo!s}][repository]'.format(repo=repo)
        branch = 'data[repositories][{repo!s}][branch]'.format(repo=repo)
        if parameters[repository] and parameters[branch]:
            json_data.append({
                'urlRepo': parameters[repository],
                'branch': parameters[branch]
            })
            email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                .format(repository=parameters[repository], branch=parameters[branch])
            email_data.append({"urlEnv": email_text})
    add_repo = integrates_dao.add_list_resource_dynamo(
        project,
        json_data,
        "repositories"
    )
    if add_repo:
        to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
        context = {
            'project': project.upper(),
            'user_email': request.session["username"],
            'action': 'Add repositories',
            'resources': email_data,
            'project_url': '{url!s}/dashboard#!/project/{project!s}/resources'
            .format(url=BASE_URL, project=project)
        }
        send_mail_repositories(to, context)
        return util.response([], 'Success', False)
    else:
        rollbar.report_message('Error: An error occurred adding repository', 'error', request)
        return util.response([], 'Error', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def remove_repositories(request):
    """Remove repositories to proyect."""
    parameters = request.POST.dict()
    project = parameters["project"]
    repository = parameters["data[urlRepo]"]
    branch = parameters["data[branch]"]
    project_info = integrates_dao.get_project_dynamo(project)
    repo_list = project_info[0]["repositories"]
    index = -1
    cont = 0
    email_data = []
    while index < 0 and len(repo_list) > cont:
        if repo_list[cont]["urlRepo"] == repository and repo_list[cont]["branch"] == branch:
            email_text = 'Repository: {repository!s} Branch: {branch!s}' \
                .format(repository=repository, branch=branch)
            email_data.append({"urlEnv": email_text})
            index = cont
        else:
            index = -1
        cont += 1
    if index >= 0:
        remove_repo = integrates_dao.remove_list_resource_dynamo(project, "repositories", index)
        if remove_repo:
            to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
            context = {
                'project': project.upper(),
                'user_email': request.session["username"],
                'action': 'Remove repositories',
                'resources': email_data,
                'project_url': '{url!s}/dashboard#!/project/{project!s}/resources'
                .format(url=BASE_URL, project=project)
            }
            send_mail_repositories(to, context)
            return util.response([], 'Success', False)
        else:
            rollbar.report_message('Error: An error occurred removing repository', 'error', request)
            return util.response([], 'Error', True)
    else:
        util.cloudwatch_log(request, 'Security: Attempted to remove repository that does not exist')
        return util.response([], 'Error', True)


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def get_environments(request):
    """Get the environments of a project."""
    project = request.GET.get('project', None)
    json_info = []
    project_info = integrates_dao.get_project_dynamo(project)
    for info in project_info:
        if "environments" in info:
            json_info = info['environments']
            break
        else:
            json_info = []
    return util.response(json_info, 'Success', False)


@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def add_environments(request):
    """Add environments to proyect."""
    parameters = request.POST.dict()
    project = parameters["project"]
    total_environments = parameters["data[totalEnv]"]
    json_data = []
    for env in range(int(total_environments)):
        environment = 'data[environments][{env!s}][environment]'.format(env=env)
        if parameters[environment]:
            json_data.append({
                'urlEnv': parameters[environment],
            })
    add_env = integrates_dao.add_list_resource_dynamo(
        project,
        json_data,
        "environments"
    )
    if add_env:
        to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
        context = {
            'project': project.upper(),
            'user_email': request.session["username"],
            'action': 'Add environments',
            'resources': json_data,
            'project_url': '{url!s}/dashboard#!/project/{project!s}/resources'
            .format(url=BASE_URL, project=project)
        }
        send_mail_repositories(to, context)
        return util.response([], 'Success', False)
    else:
        rollbar.report_message('Error: An error occurred adding environments', 'error', request)
        return util.response([], 'Error', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer', 'admin'])
@require_project_access
def remove_environments(request):
    """Remove environments to proyect."""
    parameters = request.POST.dict()
    project = parameters["project"]
    environment = parameters["data[urlEnv]"]
    project_info = integrates_dao.get_project_dynamo(project)
    repo_list = project_info[0]["environments"]
    index = -1
    cont = 0
    while index < 0 and len(repo_list) > cont:
        if repo_list[cont]["urlEnv"] == environment:
            json_data = [repo_list[cont]]
            index = cont
        else:
            index = -1
        cont += 1
    if index >= 0:
        remove_env = integrates_dao.remove_list_resource_dynamo(project, "environments", index)
        if remove_env:
            to = ['continuous@fluidattacks.com', 'projects@fluidattacks.com']
            context = {
                'project': project.upper(),
                'user_email': request.session["username"],
                'action': 'Remove environments',
                'resources': json_data,
                'project_url': '{url!s}/dashboard#!/project/{project!s}/resources'
                .format(url=BASE_URL, project=project)
            }
            send_mail_repositories(to, context)
            return util.response([], 'Success', False)
        else:
            rollbar.report_message('Error: An error occurred removing environment', 'error', request)
            return util.response([], 'Error', True)
    else:
        util.cloudwatch_log(request, 'Security: Attempted to remove environment that does not exist')
        return util.response([], 'Error', True)


@never_cache
@require_http_methods(["POST"])
@authorize(['admin'])
@require_project_access
def delete_project(request):
    """Delete project information."""
    project = request.POST.get('project', "")
    project = project.lower()
    are_users_removed = remove_all_users_access(project)
    is_project_masked = mask_project_findings(project)
    are_closings_masked = mask_project_closings(project)
    is_project_deleted = are_users_removed and is_project_masked and are_closings_masked
    if is_project_deleted:
        return util.response([], 'Success', False)
    else:
        rollbar.report_message('Error: An error occurred deleting project', 'error', request)
        return util.response([], 'Error', True)


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
        finreqset = api.get_findings(project)["submissions"]
        are_evidences_deleted = list(map(delete_s3_all_evidences, finreqset))
        is_project_masked = list(map(mask_finding, finreqset))
        is_project_deleted = all(is_project_masked) and all(are_evidences_deleted)
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
    closing_dto = ClosingDTO()
    closing_id = submission_id["id"]
    closing_dto.mask_closing(closing_id, "Masked")
    closing_dto.to_formstack()
    request = api.update(closing_dto.request_id, closing_dto.data)
    return request


def delete_s3_all_evidences(submission_id):
    """Delete s3 evidences files."""
    finding_id = submission_id["id"]
    evidences_list = key_existing_list(finding_id)
    is_evidence_deleted = False
    if evidences_list:
        is_evidence_deleted_s3 = list(map(delete_s3_evidence, evidences_list))
        if any(is_evidence_deleted_s3):
            integrates_dao.delete_finding_dynamo(finding_id)
            is_evidence_deleted = True
        else:
            rollbar.report_message(
                'Error: An error occurred deleting project evidences from s3',
                'error')
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
