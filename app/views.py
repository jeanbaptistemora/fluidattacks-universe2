# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

import os
import re
import json
import time
import pytz
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize
from .autodoc import IE, IT
from .dto.finding import FindingDTO
from .dto.closing import ClosingDTO
from .dto.eventuality import EventualityDTO
# pylint: disable=E0402
from .mailer import send_mail_delete_finding
from .mailer import send_mail_remediate_finding
from .services import has_access_to_project
from .dao import integrates_dao
from .api.drive import DriveAPI
from .api.formstack import FormstackAPI
from magic import Magic
from datetime import datetime

@never_cache
def index(request):
    "Vista de login para usuarios no autenticados"
    parameters = {}
    return render(request, "index.html", parameters)


def error500(request):
    "Vista de error"
    parameters = {}
    return render(request, "HTTP500.html", parameters)


def error401(request):
    "Vista de error"
    parameters = {}
    return render(request, "HTTP401.html", parameters)


@csrf_exempt
@never_cache
@authenticate
def registration(request):
    "Vista de registro para usuarios autenticados"
    try:
        parameters = {
            'username': request.session["username"],
            'is_registered': request.session["registered"],
        }
    except KeyError:
        return redirect('/error500')
    return render(request, "registration.html", parameters)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def dashboard(request):
    "Vista de panel de control para usuarios autenticados"
    try:
        parameters = {
            'username': request.session["username"],
            'company': request.session["company"],
            'last_login': request.session["last_login"],
        }
        integrates_dao.update_user_login_dao(request.session["username"])
    except KeyError:
        return redirect('/error500')
    return render(request, "dashboard.html", parameters)


@csrf_exempt
@authenticate
def logout(request):
    "Cierra la sesion activa de un usuario"

    HttpResponse("<script>Intercom('shutdown');</script>")
    try:
        del(request.session["username"])
        del(request.session["company"])
        del(request.session["role"])
        del(request.session["registered"])
    except KeyError:
        pass
    return redirect("/index")


# Documentacion automatica
@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def export_autodoc(request):
    "Captura y devuelve el pdf de un proyecto"
    project = request.GET.get('project', "")
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('dashboard')

    detail = {
        "IT": {
            "content_type": "application/vnd.openxmlformats\
                             -officedocument.spreadsheetml.sheet",
            "content_disposition": "inline;filename=:project.xlsx",
            "path": "/usr/src/app/app/autodoc/results/:project_:username.xlsx"
        },
        "IE": {
            "content_type": "application/vnd.openxmlformats\
                            -officedocument.presentationml.presentation",
            "content_disposition": "inline;filename=:project.pptx",
            "path": "/usr/src/app/app/autodoc/results/:project_:username.pptx"
        }
    }
    try:
        kind = request.GET.get("format", "").strip()
        if kind != "IE" != kind != "IT":
            raise Exception('This security event will be registered')
        filename = detail[kind]["path"]
        filename = filename.replace(":project", project)
        filename = filename.replace(":username", username)
        if not util.is_name(project):
            raise Exception('This security event will be registered')
        if not os.path.isfile(filename):
            raise Exception('Documentation has not been generated')
        with open(filename, 'r') as document:
            response = HttpResponse(document.read(),
                                    content_type=detail[kind]["content_type"])
            file_name = detail[kind]["content_disposition"]
            file_name = file_name.replace(":project", project)
            response['Content-Disposition'] = file_name
        return response
    except ValueError as expt:
        return HttpResponse(expt.message)
    except Exception as expt:
        return HttpResponse(expt.message)
    return HttpResponse(expt.message)


@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer'])
def generate_autodoc(request):
    "Genera la documentacion automatica"
    project = request.POST.get('project', "")
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('dashboard')

    start_time = time.time()
    data = request.POST.get('data', None)
    kind = request.POST.get('format', "")
    if kind != "IE" != kind != "IT":
        util.response([], 'Error de parametrizacion', True)
    if util.is_json(data) and util.is_name(project):
        findings = json.loads(data)
        if len(findings) >= 1:
            if kind == "IE":
                generate_autodoc_ie(request, project, findings)
            else:
                generate_autodoc_it(request, project, findings)
            str_time = str("%s" % (time.time() - start_time))
            return util.response([], 'Documentation generated in ' +
                                 str("%.2f seconds" %
                                     float(str_time)), False)
    return util.response([], 'Error...', True)


@authorize(['analyst'])
def generate_autodoc_ie(request, project, findings):
    if(findings[0]["tipo"] == "Detallado"):
        IE.Bancolombia(project, findings, request)
    else:
        IE.Fluid(project, findings, request)


@authorize(['analyst', 'customer'])
def generate_autodoc_it(request, project, findings):
    if(findings[0]["tipo"] == "Detallado"):
        IT.Bancolombia(project, findings, request)
    else:
        IT.Fluid(project, findings, request)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_eventualities(request):
    "Obtiene las eventualidades con el nombre del proyecto."
    project = request.GET.get('project', None)
    category = request.GET.get('category', None)
    username = request.session['username']
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    if not has_access_to_project(username, project):
        return util.response(dataset, 'a', True)
    if project is None:
        return util.response(dataset, 'Campos Vacios', True)
    if category == "Name":
        submissions = api.get_eventualities(project)
        frmset = submissions["submissions"]
        for row in frmset:
            submission = api.get_submission(row["id"])
            evtset = evt_dto.parse(row["id"], submission)
            if evtset['proyecto_fluid'].lower() == project.lower():
                dataset.append(evtset)
        return util.response(dataset, 'Success', False)
    elif category == "ID":
        # Only fluid can filter by id
        if "@fluid.la" not in username:
            return util.response(dataset, 'Access denied', True)
        if not project.isdigit():
            return util.response(dataset, 'Campos vacios', True)
        submission = api.get_submission(row["id"])
        evtset = evt_dto.parse(row["id"], submission)
        dataset.append(evtset)
        return util.response(dataset, 'Success', False)
    else:
        return util.response(dataset, 'Not actions', True)


@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer'])
def get_finding(request):
    submission_id = request.POST.get('id', "")
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    username = request.session['username']
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        frmset = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmset, request)
        if not has_access_to_project(username, finding['proyecto_fluid']):
            return util.response([], 'Access denied', True)
        else:
            closingreqset = api.get_closings_by_id(submission_id)["submissions"]
            findingcloseset = []
            for closingreq in closingreqset:
                frmset = api.get_submission(closingreq["id"])
                closingset = cls_dto.parse(frmset)
                findingcloseset.append(closingset)
                #El ultimo es el ultimo ciclo de cierre
                state = closingset
            finding["estado"] = state["estado"]
            if 'abiertas' in state:
                finding['cardinalidad'] = state['abiertas']
            if 'abiertas_cuales' in state:
                finding['donde'] = state['abiertas_cuales']
            else:
                if state['estado'] == 'Cerrado':
                    finding['donde'] = '-'
            if 'cerradas_cuales' in state:
                finding['cerradas'] = state['cerradas_cuales']
            finding["cierres"] = findingcloseset
            return util.response(finding, 'Success', False)
    else:
        return util.response([], 'Wrong', True)


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
# pylint: disable=R0912
# pylint: disable=R0914
def get_findings(request):
    """Captura y procesa el nombre de un proyecto para devolver
    los hallazgos."""
    project = request.GET.get('project', "")
    username = request.session['username']
    api = FormstackAPI()
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    findings = []
    if project.strip() == "":
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(username, project):
        return util.response([], 'Access denied', True)
    finreqset = api.get_findings(project)["submissions"]
    for finreq in finreqset:
        state = {'estado': 'Abierto'}
        findingset = api.get_submission(finreq["id"])
        finding = fin_dto.parse(finreq["id"], findingset, request)
        if finding['proyecto_fluid'].lower() == project.lower():
            closingreqset = api.get_closings_by_id(finreq["id"])["submissions"]
            findingcloseset = []
            for closingreq in closingreqset:
                frmset = api.get_submission(closingreq["id"])
                closingset = cls_dto.parse(frmset)
                findingcloseset.append(closingset)
                #El ultimo es el ultimo ciclo de cierre
                state = closingset
            finding["estado"] = state["estado"]
            finding["cierres"] = findingcloseset
            finding['cardinalidad_total'] = finding['cardinalidad']
            if 'abiertas' in state:
                finding['cardinalidad'] = state['abiertas']
            if 'abiertas_cuales' in state:
                finding['donde'] = state['abiertas_cuales']
            else:
                if state['estado'] == 'Cerrado':
                    finding['donde'] = '-'
            if 'cerradas_cuales' in state:
                finding['cerradas'] = state['cerradas_cuales']
            if state['estado'] == 'Cerrado':
                finding['donde'] = '-'
                finding['edad'] = '-'
            else:
                tzn = pytz.timezone('America/Bogota')
                finding_date_str = finding["timestamp"].split(" ")[0]
                finding_date = datetime.strptime(finding_date_str, '%Y-%m-%d')
                finding_date = finding_date.replace(tzinfo=tzn).date()
                current_date = datetime.now(tz=tzn).date()
                final_date = (current_date - finding_date)
                strdays = ":n".replace(":n", str(final_date.days))
                finding['edad'] = strdays
            if 'cerradas_cuales' in state:
                finding['cerradas'] = state['cerradas_cuales']
            findings.append(finding)
    findings.reverse()
    return util.response(findings, 'Success', False)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def get_evidence(request):
    drive_id = request.GET.get('id', None)
    if drive_id is None:
        return HttpResponse("Error - Unsent image ID", content_type="text/html")
    if drive_id not in request.session:
        return util.response([], 'Access denied', True)
    if not re.match("[a-zA-Z0-9_-]{20,}", drive_id):
        return HttpResponse("Error - ID with wrong format", content_type="text/html")
    drive_api = DriveAPI(drive_id)
    # pylint: disable=W0622
    if not drive_api.FILE:
        return HttpResponse("Error - Unable to download the image", content_type="text/html")
    else:
        filename = "/tmp/:id.tmp".replace(":id", drive_id)
        mime = Magic(mime=True)
        mime_type = mime.from_file(filename)
        if mime_type == "image/png":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="image/png")
        elif mime_type == "image/gif":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="image/gif")
        os.unlink(filename)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def get_evidences(request, fileid):
    drive_id = fileid
    if drive_id is None:
        return HttpResponse("Error - Unsent image ID", content_type="text/html")
    if drive_id not in request.session:
        return util.response([], 'Access denied', True)
    if not re.match("[a-zA-Z0-9_-]{20,}", drive_id):
        return HttpResponse("Error - ID with wrong format", content_type="text/html")
    drive_api = DriveAPI(drive_id)
    # pylint: disable=W0622
    if not drive_api.FILE:
        return HttpResponse("Error - Unable to download the image", content_type="text/html")
    else:
        filename = "/tmp/:id.tmp".replace(":id", drive_id)
        mime = Magic(mime=True)
        mime_type = mime.from_file(filename)
        if mime_type == "image/png":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="image/png")
        elif mime_type == "image/gif":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="image/gif")
        os.unlink(filename)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_exploit(request):
    drive_id = request.GET.get('id', None)
    if drive_id is None:
        return HttpResponse("Error - Unsent image ID", content_type="text/html")
    if drive_id not in request.session:
        return util.response([], 'Access denied', True)
    if not re.match("[a-zA-Z0-9_-]{20,}", drive_id):
        return HttpResponse("Error - ID with wrong format", content_type="text/html")
    drive_api = DriveAPI(drive_id)
    if drive_api.FILE is None:
        return HttpResponse("Error - Unable to download the file", content_type="text/html")
    filename = "/tmp/:id.tmp".replace(":id", drive_id)
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    if mime_type == "text/x-c":
        with open(filename, "r") as file_obj:
            return HttpResponse(file_obj.read(), content_type="text/plain")
    elif mime_type == "text/x-python":
        with open(filename, "r") as file_obj:
            return HttpResponse(file_obj.read(), content_type="text/plain")
    elif mime_type == "text/plain":
        with open(filename, "r") as file_obj:
            return HttpResponse(file_obj.read(), content_type="text/plain")
    elif mime_type == "text/html":
        with open(filename, "r") as file_obj:
            return HttpResponse(file_obj.read(), content_type="text/plain")
    os.unlink(filename)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_myevents(request):
    user = request.session["username"]
    projects = integrates_dao.get_projects_by_user(user)
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    for row in projects:
        project = row[0]
        submissions = api.get_eventualities(project)
        frmset = submissions["submissions"]
        for evtsub in frmset:
            submission = api.get_submission(evtsub["id"])
            evtset = evt_dto.parse(evtsub["id"], submission)
            if evtset['proyecto_fluid'].lower() == project.lower():
                if evtset['estado'] == "Pendiente":
                    dataset.append(evtset)
    return util.response(dataset, 'Success', False)


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
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
@authorize(['analyst'])
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
        return util.response([], 'error', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
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
        return util.response([], 'error', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer'])
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
        return util.response([], 'error', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_eventuality(request):
    "Actualiza una eventualidad asociada a un proyecto"
    parameters = request.POST.dict()
    try:
        generic_dto = EventualityDTO()
        generic_dto.create(parameters)
        if not parameters["vuln[afectacion]"].isdigit():
            return util.response([], 'Afectacion negativa', True)
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        return util.response([], 'error', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def delete_finding(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    parameters = request.POST.dict()
    username = request.session['username']
    fin_dto = FindingDTO()
    try:
        submission_id = parameters["data[id]"]
        context = fin_dto.create_delete(parameters, username, "", "")
        api = FormstackAPI()
        frmreq = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmreq, request)
        context["project"] = finding["proyecto_fluid"]
        context["name_finding"] = finding["hallazgo"]
        result = api.delete_submission(submission_id)
        if result is None:
            return util.response([], 'Error', True)
        to = ["engineering@fluid.la"]
        send_mail_delete_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer'])
def finding_solved(request):
    """ Envia un correo solicitando la revision de un hallazgo """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    # Send email parameters
    try:
        to = [x[0] for x in recipients]
        to.append('concurrent@fluid.la')
        to.append('projects@fluid.la')
        context = {
           'project': parameters['data[project]'],
           'finding_name': parameters['data[finding_name]'],
           'user_mail': parameters['data[user_mail]'],
           'finding_url': parameters['data[finding_url]'],
           'finding_id': parameters['data[finding_id]'],
           'finding_vulns': parameters['data[finding_vulns]'],
           'company': request.session["company"],
            }
        send_mail_remediate_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        return util.response([], 'Campos vacios', True)
