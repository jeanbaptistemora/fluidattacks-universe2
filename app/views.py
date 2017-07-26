# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

import os
import json
import time
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize
from .models import FormstackAPI, FormstackRequestMapper
from .autodoc import IE, IT
# pylint: disable=E0402
from .mailer import send_mail_delete_finding
from .services import has_access_to_project
from .dao import integrates_dao

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
            'company': request.session["company"]
        }
        integrates_dao.update_user_login_dao(request.session["username"])
    except KeyError:
        return redirect('/error500')
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
            raise Exception('Este evento de seguridad sera registrado')
        filename = detail[kind]["path"]
        filename = filename.replace(":project", project)
        filename = filename.replace(":username", username)
        if not util.is_name(project):
            raise Exception('Este evento de seguridad sera registrado')
        if not os.path.isfile(filename):
            raise Exception('La documentacion no ha sido generada')
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
            return util.response([], 'Documentacion generada en ' +
                                 str("%.2f segundos" %
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
@authorize(['analyst', 'customer'])
def get_findings(request):
    """Captura y procesa el nombre de un proyecto para devolver
    los hallazgos."""
    project = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('dashboard')

    filtr = request.GET.get('filter', None)
    if not project:
        return util.response([], 'Empty fields', True)
    if project.strip() == "":
        return util.response([], 'Empty fields', True)
    api = FormstackAPI()
    finding_requests = api.get_findings(project)["submissions"]
    # pylint: disable=C1801
    if len(finding_requests) == 0:
        return util.response([], 'El proyecto no existe', False)
    findings = []
    rmp = FormstackRequestMapper()
    for finding in finding_requests:
        formstack_request = api.get_submission(finding["id"])
        finding_parsed = rmp.map_finding(formstack_request)
        state = api.get_finding_state(finding["id"])
        finding_parsed['estado'] = state['estado']
        if 'abiertas' in state:
            finding_parsed['cardinalidad'] = state['abiertas']
        if not filtr:
            findings.append(finding_parsed)
        elif "tipo_prueba" in finding_parsed:
            if filtr.encode("utf8") == \
                    finding_parsed["tipo_prueba"].encode("utf8"):
                findings.append(finding_parsed)
    findings.reverse()
    return util.response(findings, 'Success', False)


@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def get_finding(request):
    submission_id = request.POST.get('id', None)
    if util.is_numeric(submission_id):
        api = FormstackAPI()
        rmp = FormstackRequestMapper()
        formstack_request = api.get_submission(submission_id)
        finding = rmp.map_finding(formstack_request)

        username = request.session['username']
        if not has_access_to_project(username, finding['proyecto_fluid']):
            return redirect('dashboard')

        state = api.get_finding_state(submission_id)
        finding['estado'] = state['estado']
        if 'abiertas' in state:
            finding['cardinalidad'] = state['abiertas']
        if 'abiertas_cuales' in state:
            finding['donde'] = state['abiertas_cuales']
        return util.response(finding, 'Success', False)
    return util.response([], 'Empty fields', True)


@never_cache
@csrf_exempt
@authorize(['analyst'])
def get_eventualities(request):
    """Obtiene las eventualidades con el nombre del proyecto."""
    project = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project):
        return redirect('dashboard')

    category = request.GET.get('category', None)
    if not category:
        category = "Name"
    if not project:
        return util.response([], 'Campos vacios', True)
    else:
        if project.strip() == "":
            return util.response([], 'Campos vacios', True)
        else:
            api = FormstackAPI()
            rmp = FormstackRequestMapper()
            if category == "Name":
                eventuality_requests = \
                    api.get_eventualities(project)["submissions"]
                if eventuality_requests:
                    # pylint: disable=C1801
                    if len(eventuality_requests) == 0:
                        return util.response([],
                                             'Este proyecto no tiene \
eventualidades o no existe', False)
                    eventualities = []
                    for eventuality in eventuality_requests:
                        eventuality_request = \
                            api.get_submission(eventuality["id"])
                        eventuality_parsed = \
                            rmp.map_eventuality(eventuality_request)
                        eventualities.append(eventuality_parsed)
                    return util.response(eventualities, 'Correcto', False)
                else:
                    return util.response([],
                                         'Este proyecto no tiene \
eventualidades o no existe', False)
            else:
                if util.is_numeric(project):
                    eventualities = []
                    eventuality_request = api.get_submission(project)
                    eventuality_parsed = \
                        rmp.map_eventuality(eventuality_request)
                    eventualities.append(eventuality_parsed)
                    return util.response(eventualities, 'Correcto', False)
                return util.response([], 'Debes ingresar un ID \
numerico!', True)


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
        api = FormstackAPI()
        rmp = FormstackRequestMapper()
        submission_id = post_parms["vuln[id]"]
        formstack_request = api.get_submission(submission_id)
        finding = rmp.map_finding(formstack_request)

        username = request.session['username']
        if not has_access_to_project(username, finding['proyecto_fluid']):
            return redirect('dashboard')

        res = api.delete_finding(submission_id)
        if res:
            finding_id = post_parms["vuln[id]"]
            finding = post_parms["vuln[hallazgo]"]
            justify = post_parms["vuln[justificacion]"]
            analyst = request.session["username"]
            context = {
                'mail_analista': analyst,
                'name_finding': finding,
                'id_finding': finding_id,
                'description': justify,
                }
            to = ["engineering@fluid.la"]
            send_mail_delete_finding(to, context)
            return util.response([], 'Eliminado correctamente!', False)
        return util.response([], 'No se pudo actualizar',
                             True)


@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst'])
def get_order(request):
    """ Obtiene de formstack el id de pedido relacionado con un proyecto """
    project_name = request.GET.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project_name):
        return redirect('dashboard')

    if util.is_name(project_name):
        api = FormstackAPI()
        order_id = api.get_order(project_name)
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
        return util.response([], 'No se pudo consultar', True)
    return util.response([], 'Campos vacios', True)


@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_order(request):
    """ Actualiza el nombre de proyecto del id de pedido relacionado """
    project_name = request.POST.get('project', None)
    username = request.session['username']

    if not has_access_to_project(username, project_name):
        return redirect('dashboard')

    order_id = request.POST.get('id', None)
    if not util.is_name(project_name):
        return util.response([], 'Campos vacios', True)
    if not util.is_numeric(order_id):
        return util.response([], 'Campos vacios', True)
    api = FormstackAPI()
    updated = api.update_order(project_name, order_id)
    if not updated:
        return util.response([], 'No se pudo actualizar',
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
    api = FormstackAPI()
    submission_id = post_parms["vuln[id]"]
    afectacion = post_parms["vuln[afectacion]"]
    updated = api.update_eventuality(afectacion, submission_id)
    if not updated:
        return util.response([], 'No se pudo actualizar',
                             True)
    return util.response([], 'Actualizado correctamente!', False)


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
        if nivel == "Detallado":
            if "vuln[riesgo]" in post_parms:
                execute = True
        else:
            if "vuln[vector_ataque]" in post_parms \
                    and "vuln[sistema_comprometido]" in post_parms:
                execute = True
        if not execute:
            return util.response([], 'Campos vacios', True)
        formstack_api = FormstackAPI()
        submission_id = post_parms["vuln[id]"]
        rmp = FormstackRequestMapper()
        formstack_request = formstack_api.get_submission(submission_id)
        finding = rmp.map_finding(formstack_request)

        username = request.session['username']
        if not has_access_to_project(username, finding['proyecto_fluid']):
            return redirect('dashboard')

        updated = formstack_api.update_finding(post_parms, submission_id)
        if not updated:
            return util.response([], 'No se pudo actualizar',
                                 True)
        return util.response([], 'Actualizado correctamente!', False)
