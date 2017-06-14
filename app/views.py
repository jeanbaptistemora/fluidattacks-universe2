# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

import os
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize
from .models import FormstackAPI, FormstackRequestMapper
from autodoc import IE, IT
import time
# pylint: disable=E0402
from .mailer import Mailer
from .services import has_access_to_project
from .dao import integrates_dao


def index(request):
    "Vista de login para usuarios no autenticados"
    parameters = {}
    return render(request, "index.html", parameters)


@csrf_exempt
@authenticate
def registration(request):
    "Vista de registro para usuarios autenticados"
    parameters = {
        'username': request.session["username"]
    }
    try:
        if request.session["registered"] == '1':
            return redirect("/dashboard")
        return render(request, "registration.html", parameters)
    except KeyError:
        pass
    return redirect("/index")

@csrf_exempt
@authorize(['analyst', 'customer'])
def dashboard(request):
    "Vista de panel de control para usuarios autenticados"
    parameters = {
        'username': request.session["username"],
        'company': request.session["company"]
    }
    integrates_dao.update_user_login_dao(request.session["username"])
    return render(request, "dashboard.html", parameters)


@csrf_exempt
@authenticate
def logout(request):
    "Cierra la sesion activa de un usuario"

    try:
        del(request.session["username"])
        del(request.session["company"])
        del(request.session["role"])
        del(request.session["registered"])
    except KeyError:
        pass
    return redirect("/index")


# Documentacion automatica
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst'])
def export_autodoc(request):
    "Captura y devuelve el pdf de un proyecto"
    project = request.GET.get('project', "")
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('/dashboard')

    detail = {
        "IT": {
            "content_type": "application/vnd.openxmlformats\
                             -officedocument.spreadsheetml.sheet",
            "content_disposition": "inline;filename=:P.xlsx",
            "path": "/usr/src/app/app/autodoc/results/:P.xlsx"
        },
        "IE": {
            "content_type": "application/vnd.openxmlformats\
                            -officedocument.presentationml.presentation",
            "content_disposition": "inline;filename=:P.pptx",
            "path": "/usr/src/app/app/autodoc/results/:P.pptx"
        }
    }
    try:
        kind = request.GET.get("format", "").strip()
        if kind != "IE" != kind != "IT":
            raise Exception('Este evento de seguridad sera registrado')
        filename = detail[kind]["path"].replace(":P", project)
        if not util.is_name(project):
            raise Exception('Este evento de seguridad sera registrado')
        if not os.path.isfile(filename):
            raise Exception('La documentacion no ha sido generada')
        with open(filename, 'r') as document:
            response = HttpResponse(document.read(),
                                    content_type=detail[kind]["content_type"])
            response['Content-Disposition'] = \
                detail[kind]["content_disposition"].replace(":P", project)
        return response
    except ValueError as expt:
        return HttpResponse(expt.message)
    except Exception as expt:
        return HttpResponse(expt.message)
    return HttpResponse(expt.message)


@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst'])
def generate_autodoc(request):
    "Genera la documentacion automatica en excel"
    project = request.POST.get('project', "")
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('/dashboard')

    start_time = time.time()
    data = request.POST.get('data', None)
    kind = request.POST.get('format', "")
    if kind != "IE" != kind != "IT":
        util.response([], 'Error de parametrizacion', True)
    if util.is_json(data) and util.is_name(project):
        findings = json.loads(data)
        if len(findings) >= 1:
            if kind == "IE":
                if(findings[0]["tipo"] == "Detallado"):
                    IE.Bancolombia(project, findings)
                else:
                    IE.Fluid(project, findings)
            else:
                if(findings[0]["tipo"] == "Detallado"):
                    IT.Bancolombia(project, findings)
                else:
                    IT.Fluid(project, findings)
            str_time = str("%s" % (time.time() - start_time))
            return util.response([], 'Documentacion generada en ' +
                                 str("%.2f segundos" %
                                     float(str_time)), False)
    return util.response([], 'Error...', True)


@csrf_exempt
@authorize(['analyst', 'customer'])
def get_findings(request):
    """Captura y procesa el nombre de un proyecto para devolver
    los hallazgos."""
    project = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('/dashboard')

    filtr = request.GET.get('filter', None)
    if not project:
        return util.response([], 'Empty fields', True)
    if project.strip() == "":
        return util.response([], 'Empty fields', True)
    API = FormstackAPI()
    finding_requests = API.get_findings(project)["submissions"]
    # pylint: disable=C1801
    if len(finding_requests) == 0:
        return util.response([], 'El proyecto no existe', False)
    findings = []
    RMP = FormstackRequestMapper()
    for finding in finding_requests:
        formstack_request = API.get_submission(finding["id"])
        finding_parsed = RMP.map_finding(formstack_request)
        if not filtr:
            findings.append(finding_parsed)
        elif "tipo_prueba" in finding_parsed:
            if filtr.encode("utf8") == \
                    finding_parsed["tipo_prueba"].encode("utf8"):
                findings.append(finding_parsed)
    return util.response(findings, 'Success', False)


# FIXME: Need to add access control to this function
@csrf_exempt
@authorize(['analyst', 'customer'])
def get_finding(request):
    project_id = request.POST.get('id', None)
    if util.is_numeric(project_id):
        API = FormstackAPI()
        RMP = FormstackRequestMapper()
        formstack_request = API.get_submission(project_id)
        finding = RMP.map_finding(formstack_request)
        return util.response(finding, 'Success', False)
    return util.response([], 'Empty fields', True)


@csrf_exempt
@authorize(['analyst'])
def get_eventualities(request):
    """Obtiene las eventualidades con el nombre del proyecto."""
    project = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('/dashboard')

    category = request.GET.get('category', None)
    if not category:
        category = "Name"
    if not project:
        return util.response([], 'Campos vacios', True)
    else:
        if project.strip() == "":
            return util.response([], 'Campos vacios', True)
        else:
            API = FormstackAPI()
            RMP = FormstackRequestMapper()
            if category == "Name":
                eventuality_requests = \
                    API.get_eventualities(project)["submissions"]
                if eventuality_requests:
                    # pylint: disable=C1801
                    if len(eventuality_requests) == 0:
                        return util.response([],
                                             'Este proyecto no tiene \
eventualidades o no existe', False)
                    eventualities = []
                    for eventuality in eventuality_requests:
                        eventuality_request = \
                            API.get_submission(eventuality["id"])
                        eventuality_parsed = \
                            RMP.map_eventuality(eventuality_request)
                        eventualities.append(eventuality_parsed)
                    return util.response(eventualities, 'Correcto', False)
                else:
                    return util.response([],
                                         'Este proyecto no tiene \
eventualidades o no existe', False)
            else:
                if util.is_numeric(project):
                    eventualities = []
                    eventuality_request = API.get_submission(project)
                    eventuality_parsed = \
                        RMP.map_eventuality(eventuality_request)
                    eventualities.append(eventuality_parsed)
                    return util.response(eventualities, 'Correcto', False)
                return util.response([], 'Debes ingresar un ID \
numerico!', True)


# FIXME: Need to add access control to this function
@csrf_exempt
@authorize(['analyst'])
def delete_finding(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    post_parms = request.POST.dict()
    if "vuln[hallazgo]" not in post_parms \
        or "vuln[proyecto_fluid]" not in post_parms \
        or "vuln[justificacion]" not in post_parms \
            or "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        API = FormstackAPI()
        submission_id = post_parms["vuln[id]"]
        res = API.delete_finding(submission_id)
        if res:
            finding_id = post_parms["vuln[id]"]
            finding = post_parms["vuln[hallazgo]"]
            justify = post_parms["vuln[justificacion]"]
            analyst = request.session["username"]
            send_mail = Mailer()
            send_mail.send_delete_finding(finding_id, finding, analyst, justify)
            send_mail.close()
            return util.response([], 'Eliminado correctamente!', False)
        return util.response([], 'No se pudo actualizar formstack',
                             True)


@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst'])
def get_order(request):
    """ Obtiene de formstack el id de pedido relacionado con un proyecto """
    project_name = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project_name):
        return redirect('/dashboard')

    if util.is_name(project_name):
        API = FormstackAPI()
        order_id = API.get_order(project_name)
        if "submissions" in order_id:
            # pylint: disable=C1801
            if len(order_id["submissions"]) == 1:
                return util.response(order_id["submissions"][0]["id"],
                                     'Consulta exitosa!', False)
            # pylint: disable=C1801
            elif len(order_id["submissions"]) == 0:
                return util.response("0",
                                     'No se ha asignado un pedido!',
                                     False)
            return util.response([], 'Este proyecto tiene varios IDs',
                                 True)
        return util.response([], 'No se pudo consultar formstack', True)
    return util.response([], 'Campos vacios', True)


@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_order(request):
    """ Actualiza el nombre de proyecto del id de pedido relacionado """
    project_name = request.POST.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project_name):
        return redirect('/dashboard')

    order_id = request.POST.get('id', None)
    if not util.is_name(project_name):
        return util.response([], 'Campos vacios', True)
    if not util.is_numeric(order_id):
        return util.response([], 'Campos vacios', True)
    API = FormstackAPI()
    updated = API.update_order(project_name, order_id)
    if not updated:
        return util.response([], 'No se pudo actualizar formstack',
                             True)
    return util.response([], 'Actualizado correctamente!', False)


# FIXME: Need to add access control to this function
@csrf_exempt
@authorize(['analyst'])
def update_eventuality(request):
    "Captura y procesa los parametros para actualizar una eventualidad"
    post_parms = request.POST.dict()

    if "vuln[proyecto_fluid]" not in post_parms \
        != "vuln[id]" not in post_parms \
            != "vuln[afectacion]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        validate = False
        try:
            int(post_parms["vuln[afectacion]"])
            validate = True
        except ValueError:
            validate = False
        if not validate:
            return util.response([], 'Afectacion negativa', True)
    API = FormstackAPI()
    submission_id = post_parms["vuln[id]"]
    afectacion = post_parms["vuln[afectacion]"]
    updated = API.update_eventuality(afectacion, submission_id)
    if not updated:
        return util.response([], 'No se pudo actualizar formstack',
                             True)
    return util.response([], 'Actualizado correctamente!', False)


# FIXME: Need to add access control to this function
@csrf_exempt
@authorize(['analyst'])
def update_finding(request):
    "Captura y procesa los parametros para actualizar un hallazgo"
    post_parms = request.POST.dict()
    if "vuln[proyecto_fluid]" not in post_parms \
        != "vuln[nivel]" not in post_parms \
        != "vuln[hallazgo]" not in post_parms \
        != "vuln[vulnerabilidad]" not in post_parms \
        != "vuln[donde]" not in post_parms \
        != "vuln[cardinalidad]" not in post_parms \
        != "vuln[criticidad]" not in post_parms \
        != "vuln[amenaza]" not in post_parms \
        != "vuln[requisitos]" not in post_parms \
            != "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        nivel = post_parms["vuln[nivel]"]
        execute = False
        if nivel == "General":
            if "vuln[vector_ataque]" in post_parms \
                    and "vuln[sistema_comprometido]" in post_parms:
                execute = True
        else:
            if "vuln[riesgo]" in post_parms:
                execute = True
        if not execute:
            return util.response([], 'Campos vacios', True)
        formstack_api = FormstackAPI()
        submission_id = post_parms["vuln[id]"]
        updated = formstack_api.update_finding(post_parms, submission_id)
        if not updated:
            return util.response([], 'No se pudo actualizar formstack',
                                 True)
        return util.response([], 'Actualizado correctamente!', False)
