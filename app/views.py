""" Vistas y servicios para FluidIntegrates """
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models, response
import logging

USER = "glopez@fluid.la"

def index(request):
    "Vista de login para usuarios no autenticados"
    parameters = {}
    return render(request, "index.html", parameters)

@csrf_exempt
def dashboard(request):
    "Vista de panel de control para usuarios autenticados"
    parameters = {}
    return render(request, "dashboard.html", parameters)

@csrf_exempt
def login(request):
    "Captura los parametros para la autenticacion"
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not username or not password:
        return response.send([], 'Empty fields', True)
    else:
        result = models.one_login_auth(username, password)
        if result["status"]["type"] == "success":
            request.session['username'] = username
            return response.send([], 'Success', False)
        else:
            return response.send([], 'Wrong! Username/Password', True)

@csrf_exempt
def get_vuln_by_name(request):
    "Captura y procesa el nombre de un proyecto para devolver los hallazgos"
    project = request.GET.get('project', None)
    logging.info("TAREA: %s, USUARIO: %s", "Consultando proyecto "+project, USER)
    if not project:
        return response.send([], 'Empty fields', True)
    else:
        if project.strip() == "":
            return response.send([], 'Empty fields', True)
        else:
            result = models.get_vuln_by_name(project)["submissions"]
            if len(result) == 0:
                return response.send([], 'Project doesn\'t exist', True)
            else:
                ids = []
                vulns = []
                for i in result:
                    ids.append(i["id"])
                for j in ids:
                    vuln = models.get_vuln_by_submission_id(j)
                    vulns.append(vuln)
                return response.send(vulns, 'Success', False)

@csrf_exempt
def get_vuln_by_date(request):
    "Obtiene la fecha min y max para consultar los hallazgos en ese rango"
    from_date = request.GET.get('from', None)
    to_date = request.GET.get('tp', None)
    if not from_date or not to_date:
        return response.send([], 'Empty fields', True)
    else:
        if from_date.strip() == "" or to_date.strip() == "":
            return response.send([], 'Empty fields', True)
        else:
            return HttpResponse("TEST2")

@csrf_exempt
def get_evnt_by_name(request):
    """Obtiene las eventualidades con el nombre del proyecto"""
    project = request.GET.get('project', None)
    if not project:
        return response.send([], 'Empty fields', True)
    else:
        if project.strip() == "":
            return response.send([], 'Empty fields', True)
        else:
            return HttpResponse("TEST3")

@csrf_exempt
def update_vuln(request):
    "Captura y procesa los parametros para actualizar un hallazgo"
    post_parms = request.POST.dict()
    proj = "No enviado"
    id = ""
    if "vuln[proyecto_fluid]" not in post_parms:
        return response.send([], 'Campos vacios', True)
    elif "vuln[id]" not in post_parms:
        return response.send([], 'Campos vacios', True)
    else:
        id = post_parms["vuln[id]"]
        proj = post_parms["vuln[proyecto_fluid]"] + "["+id+"]"
    csrf = True
    logging.info("TAREA: %s, USUARIO: %s", "Actualizando proyecto "+ proj, USER)
    if csrf == False:
        return response.send([], 'CSRF', True)
    else:
        updated = models.update_vuln_by_id(post_parms)
        if updated == {}:
            return response.send([], 'Hubo un error', True)
        else:
            if  hasattr(updated, 'text'):
                res = json.loads(updated.text)
                if "success" in res:
                    logging.info("TAREA: %s, USUARIO: %s", "Actualizacion completada, PROYECTO: " + proj, USER)
                    return response.send([], 'Success', False)
                else:
                    return response.send([], 'No se pudo actualizar formstack', True)
            else:
                return response.send([], 'No se pudo actualizar formstack', True)

@csrf_exempt
def delete_vuln(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    post_parms = request.POST.dict()
    csrf = True
    if csrf == False:
        return response.send([], 'CSRF', True)
    else:
        res = models.delete_vuln_by_id(post_parms, USER)
        if res:
            return response.send([], 'Eliminado correctamente!', False)
        else:
            return response.send([], 'No se pudo actualizar formstack', False)
