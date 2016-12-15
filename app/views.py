# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

import os
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse
from . import models, util
from autodoc import IE, IT
import time

def index(request):
    "Vista de login para usuarios no autenticados"
    parameters = {}
    return render(request, "index.html", parameters)

@csrf_exempt
def dashboard(request):
    "Vista de panel de control para usuarios autenticados"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized <script>location = "/index"; </script>', status=401)
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
            return util.response([], 'Bienvenido ' + username, False)
        else:
            return util.response([], 'Usuario/Clave incorrectos', True)

# Documentacion automatica
@csrf_exempt
@require_http_methods(["GET"])
def export_autodoc(request):
    "Captura y devuelve el pdf de un proyecto"
    detail = {
        "IT": {
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "content_disposition": "inline;filename=:P.xlsx",
            "path": "/var/www/fluid-integrates/app/autodoc/results/:P.xlsx"
        },
        "IE": {
            "content_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation" ,
            "content_disposition": "inline;filename=:P.pptx",
            "path": "/var/www/fluid-integrates/app/autodoc/results/:P.pptx"
        }
    }
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    try:
        kind = request.GET.get("format", "").strip()
        project = request.GET.get('project', "")
        if kind != "IE" != kind != "IT":
            raise Exception('Este evento de seguridad sera registrado')
        filename = detail[kind]["path"].replace(":P",project)
        if not util.is_name(project):
            raise Exception('Este evento de seguridad sera registrado')
        if not os.path.isfile(filename):
            raise Exception('La documentacion no ha sido generada')
        with open(filename, 'r') as document:
            response = HttpResponse(document.read(), content_type=detail[kind]["content_type"])
            response['Content-Disposition'] = detail[kind]["content_disposition"].replace(":P",project)
        return response
    except ValueError as expt:
        return HttpResponse(expt.message)
    except Exception as expt:
        return HttpResponse(expt.message)
    return HttpResponse(message)

@csrf_exempt
@require_http_methods(["POST"])
def generate_autodoc(request):
    "Genera la documentacion automatica en excel"
    start_time = time.time()
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    project = request.POST.get('project', "")
    data = request.POST.get('data', None)
    kind = request.POST.get('format',"")
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
            return util.response([], 'Documentacion generada en ' + str("%.2f segundos" % float(str_time)), False)
    return util.response([], 'Error...', True)

@csrf_exempt
def get_vuln_by_name(request):
    "Captura y procesa el nombre de un proyecto para devolver los hallazgos"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized <script>location = "/index"; </script>', status=401)
    project = request.GET.get('project', None)
    filtr = request.GET.get('filter', None)
    if not project:
        return util.response([], 'Empty fields', True)
    else:
        if project.strip() == "":
            return util.response([], 'Empty fields', True)
        else:
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
                    if not filtr:
                        vulns.append(vuln)
                    elif "tipo_prueba" in vuln:
                        if filtr.encode("utf8") == vuln["tipo_prueba"].encode("utf8"):
                            vulns.append(vuln)
                return util.response(vulns, 'Success', False)

@csrf_exempt
def get_vuln_by_id(request):
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized <script>location = "/index"; </script>', status=401)
    project_id = request.POST.get('id', None)
    if util.is_numeric(project_id):
        vuln = models.get_vuln_by_submission_id(project_id)
        return util.response(vuln, 'Success', False)
    else:
        return util.response([], 'Empty fields', True)

@csrf_exempt
def get_evnt_by_name(request):
    """Obtiene las eventualidades con el nombre del proyecto"""
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    project = request.GET.get('project', None)
    category = request.GET.get('category', None)
    if not category:
        category = "Name"
    if not project:
        return util.response([], 'Campos vacios', True)
    else:
        if project.strip() == "":
            return util.response([], 'Campos vacios', True)
        else:
            if category == "Name":
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
            else:
                if util.is_numeric(project):
                    evtns = []
                    evtn = models.get_evnt_by_submission_id(project)
                    if evtn:
                        evtns.append(evtn)
                        return util.response(evtns, 'Success', False)
                    else:
                        return util.response([], 'Error!', True)
                else:
                    return util.response([], 'Debes ingresar un ID numerico!', True)

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
        util.traceability(action.encode('utf-8'), request.session["username"])
        return util.response([], 'Actualizado correctamente', False)
    else:
        return util.response([], 'No se pudo actualizar formstack', True)

@csrf_exempt
def update_vuln(request):
    "Captura y procesa los parametros para actualizar un hallazgo"
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized', status=401)
    post_parms = request.POST.dict()
    action = ""
    for i,k in post_parms.items():
        post_parms[i] = k.encode('utf8')
    if "vuln[proyecto_fluid]" not in post_parms \
        or "vuln[nivel]" not in post_parms \
        or "vuln[hallazgo]" not in post_parms \
        or "vuln[vulnerabilidad]" not in post_parms \
        or "vuln[donde]" not in post_parms \
        or "vuln[cardinalidad]" not in post_parms \
        or "vuln[criticidad]" not in post_parms \
        or "vuln[amenaza]" not in post_parms \
        or "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        nivel = post_parms["vuln[nivel]"]
        execute = False
        if nivel == "General":
            if "vuln[vector_ataque]" in post_parms \
                and "vuln[sistema_comprometido]" in post_parms:
                execute = True
        elif nivel == "Detallado":
            if "vuln[riesgo]" in post_parms:
                execute = True
        else:
            execute = False
        if not execute:
            return util.response([], 'Campos vacios', True)
        res = models.update_vuln_by_id(post_parms)
        if res:
            return util.response([], 'Actualizado correctamente!', False)
        else:
            return util.response([], 'No se pudo actualizar formstack', True)

@csrf_exempt
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
        res = models.delete_vuln_by_id(post_parms["vuln[id]"])
        if res:
            #util.traceability(action, request.session["username"])
            return util.response([], 'Eliminado correctamente!', False)
        else:
            return util.response([], 'No se pudo actualizar formstack', True)
        
@csrf_exempt
@require_http_methods(["GET"])
def get_order (request):
    """ Obtiene de formstack el id de pedido relacionado con un proyecto """
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized <script>location = "/index"; </script>', status=401)
    project_name = request.GET.get('project', None)
    if util.is_name(project_name):
        order_id = models.get_order(project_name)
        if "submissions" in order_id:
            if len(order_id["submissions"]) == 1:
                return util.response(order_id["submissions"][0]["id"], 'Consulta exitosa!', False)
            elif len(order_id["submissions"]) == 0: 
                return util.response("0", 'No se ha asignado un pedido!', False)
            else:
                return util.response([], 'Este proyecto tiene varios IDs', True)
        else:
            return util.response([], 'No se pudo consultar formstack', True)
    else:
        return util.response([], 'Campos vacios', True)

@csrf_exempt
@require_http_methods(["POST"])
def update_order_id (request):
    """ Actualiza el nombre de proyecto del id de pedido relacionado """
    if not util.is_authenticated(request):
        return HttpResponse('Unauthorized <script>location = "/index"; </script>', status=401)
    project_name = request.POST.get('project', None)
    order_id = request.POST.get('id', None)
    if not util.is_name(project_name):
        return util.response([], 'Campos vacios', True)
    if not util.is_numeric(order_id): 
        return util.response([], 'Campos vacios', True)
    updated = models.update_order_id(project_name, order_id)
    if updated is None:
        return util.response([], 'No se pudo actualizar formstack', True)
    elif updated.status_code == 404:
        return util.response([], 'Ese pedido no existe', True)
    else:
        return util.response([], 'Actualizado correctamente!', False)
        
    
    