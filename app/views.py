# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

import os
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import docs
from . import models, util

USER = "glopez@fluid.la"

def index(request):
    "Vista de login para usuarios no autenticados"
    parameters = {}
    return render(request, "index.html", parameters)

@csrf_exempt
def dashboard(request):
    "Vista de panel de control para usuarios autenticados"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    parameters = {
        'username': request.session["username"]
    }
    return render(request, "dashboard.html", parameters)

@csrf_exempt
def logout(request):
    "Cierra la sesion activa de un usuario"
    request.session["username"] = None
    return redirect("/index")

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    "Captura los parametros para la autenticacion"
    username = request.POST.get('user', None)
    password = request.POST.get('pass', None)
    if not username or not password:
        return util.response([], 'Usuario/Clave son obligatorios', True)
    else:
        auth = models.one_login_auth(username, password)
        if auth:
            request.session['username'] = username
            return util.response([], 'Bienvenido '+username, False)
        else:
            return util.response([], 'Usuario/Clave incorrectos', True)

# Documentacion automatica
@csrf_exempt
@require_http_methods(["GET"])
def export_autodoc(request):
    "Captura y devuelve el pdf de un proyecto"
    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    message = "Documentacion no generada"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    try:
        project = request.GET.get('project', "")
        filename = "app/autodoc/results/:proj.xlsx".replace(":proj", project)
        if util.is_name(project) and os.path.isfile(filename):
            with open(filename, 'r') as pdf:
                response = HttpResponse(pdf.read(), content_type=content_type)
                response['Content-Disposition'] = 'inline;filename='+project+'.xlsx'
                return response
    except ValueError as expt:
        return HttpResponse(expt.message)
    return HttpResponse(message)

@csrf_exempt
@require_http_methods(["POST"])
def generate_autodoc(request):
    "Genera la documentacion automatica en excel"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    project = request.POST.get('project', "")
    data = request.POST.get('data', None)
    if util.is_json(data) and util.is_name(project):
        if len(json.loads(data)) >= 1:
            docs.generate_doc_xls(project, json.loads(data))
            return util.response([], 'Documentacion generada correctamente!', False)
    return util.response([], 'Error...', True)

@csrf_exempt
def get_vuln_by_name(request):
    "Captura y procesa el nombre de un proyecto para devolver los hallazgos"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    project = request.GET.get('project', None)
    if not project:
        return util.response([], 'Empty fields', True)
    else:
        if project.strip() == "":
            return util.response([], 'Empty fields', True)
        else:
            util.traceability("Consultando proyecto "+ project, USER)
            result = models.get_vuln_by_name(project)["submissions"]
            if len(result) == 0:
                return util.response([], 'Project doesn\'t exist', True)
            else:
                ids = []
                vulns = []
                for i in result:
                    ids.append(i["id"])
                for j in ids:
                    vuln = models.get_vuln_by_submission_id(j)
                    vulns.append(vuln)
                return util.response(vulns, 'Success', False)

@csrf_exempt
def get_evnt_by_name(request):
    """Obtiene las eventualidades con el nombre del proyecto"""
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    project = request.GET.get('project', None)
    if not project:
        return util.response([], 'Campos vacios', True)
    else:
        if project.strip() == "":
            return util.response([], 'Campos vacios', True)
        else:
            util.traceability("Consultando eventualidades de proyecto "+ project, USER)
            result = models.get_evnt_by_name(project)
            if result:
                if int(result["total"]) == 0:
                    return util.response([], 'Este proyecto no tiene eventualidades', False)
                else:
                    ids, evtns = [], []
                    for i in result["submissions"]:
                        ids.append(i["id"])
                    for j in ids:
                        evtn = models.get_evnt_by_submission_id(j)
                        evtns.append(evtn)
                    return util.response(evtns, 'Success', False)
            else:
                return util.response([], 'Error!', True)

@csrf_protect
def update_evnt(request):
    "Captura y procesa los parametros para actualizar una eventualidad"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    post_parms = request.POST.dict()
    action = ""
    if "vuln[proyecto_fluid]" not in post_parms \
        or "vuln[tipo]" not in post_parms \
        or "vuln[id]" not in post_parms \
        or "vuln[afectacion]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        validate = False
        afect = 0
        try:
            afect = int(post_parms["vuln[afectacion]"])
            validate = True
        except SyntaxError:
            validate = False
        if not validate:
            return util.response([], 'Afectacion negativa', True)
        action = "Actualizar eventualidad del proyecto " \
            + post_parms["vuln[proyecto_fluid]"] \
            + " de tipo '" + post_parms["vuln[tipo]"] + "' con afectacion ("+ str(afect)+")" \
            + " [" + post_parms["vuln[id]"] + "]"
    updated = models.update_evnt_by_id(post_parms)
    if updated:
        util.traceability(action.encode('utf-8'), USER.encode('utf-8'))
        return util.response([], 'Actualizado correctamente', False)
    else:
        return util.response([], 'No se pudo actualizar formstack', True)

@csrf_protect
def update_vuln(request):
    "Captura y procesa los parametros para actualizar un hallazgo"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    post_parms = request.POST.dict()
    action = ""
    for i,k in post_parms.items():
        post_parms[i] = k.encode('utf8')
    if "vuln[proyecto_fluid]" not in post_parms \
        or "vuln[hallazgo]" not in post_parms \
        or "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        action = "Actualizar hallazgo, " \
            + post_parms["vuln[proyecto_fluid]"].upper() \
            + " => " + post_parms["vuln[hallazgo]"] \
            + "[" + post_parms["vuln[id]"] + "]"
    res = models.update_vuln_by_id(post_parms)
    if res:
        util.traceability(action, request.session["username"])
        return util.response([], 'Actualizado correctamente!', False)
    else:
        return util.response([], 'No se pudo actualizar formstack', True)

@csrf_protect
def delete_vuln(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    post_parms = request.POST.dict()
    for i,k in post_parms.items():
        post_parms[i] = k.encode('utf8')
    action = "Envio de campos vacios"
    if "vuln[hallazgo]" not in post_parms \
        or "vuln[proyecto_fluid]" not in post_parms \
        or "vuln[justificacion]" not in post_parms \
        or "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        action = "Eliminar hallazgo, " \
            + post_parms["vuln[justificacion]"] \
            + " PROYECTO " + post_parms["vuln[proyecto_fluid]"].upper() \
            + " => " + post_parms["vuln[hallazgo]"] \
            + "[" + post_parms["vuln[id]"] + "]"
        res = models.delete_vuln_by_id(post_parms["vuln[id]"])
        if res:
            util.traceability(action, request.session["username"])
            return util.response([], 'Eliminado correctamente!', False)
        else:
            return util.response([], 'No se pudo actualizar formstack', True)
        
