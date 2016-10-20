""" Vistas y servicios para FluidIntegrates """
import json,re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import models, util

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
        return util.response([], 'Empty fields', True)
    else:
        result = models.one_login_auth(username, password)
        if result["status"]["type"] == "success":
            request.session['username'] = username
            return util.response([], 'Success', False)
        else:
            return util.response([], 'Wrong! Username/Password', True)

@csrf_exempt
def generate_auto_doc(request):
    "Genera la documentacion automatica"
    project = request.POST.get('project', None)
    data = request.POST.get('data', None)
    exeq = None
    try:
        exeq = True
        if not project or not data:
            raise ValueError("")
        elif project.strip() == "":
            raise ValueError("")
        elif not re.search("^[a-zA-Z0-9]+$",project):
            raise ValueError("")
        else:
            data = json.loads(data)
    except ValueError:
        exeq = None
    finally:
        if not exeq:
            return util.response([], 'Error procesando parametros!', True)
        else:
            print project
            print data
            util.create_template(project, data)
            return util.response([], 'Success!', False)
    

@csrf_exempt
def get_vuln_by_name(request):
    "Captura y procesa el nombre de un proyecto para devolver los hallazgos"
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
                    for i in result["submissions"]: ids.append(i["id"])
                    for j in ids:
                        evtn = models.get_evnt_by_submission_id(j)
                        evtns.append(evtn)
                    return util.response(evtns, 'Success', False)
            else:
                return util.response([], 'Error!', True)

@csrf_exempt
def update_evnt(request):
    "Captura y procesa los parametros para actualizar una eventualidad"
    post_parms = request.POST.dict()
    action = ""
    if "vuln[proyecto_fluid]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    elif "vuln[tipo]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    elif "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    elif "vuln[afectacion]" not in post_parms:
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
    csrf = True
    if csrf == False:
        return util.response([], 'CSRF', True)
    else:
        print action
        updated = models.update_evnt_by_id(post_parms)
        if updated:
            print updated.text
            util.traceability(action, USER)
            return util.response([], 'Actualizado correctamente', False)
        else:
            return util.response([], 'No se pudo actualizar formstack', True)

@csrf_exempt
def update_vuln(request):
    "Captura y procesa los parametros para actualizar un hallazgo"
    post_parms = request.POST.dict()
    action = ""
    if "vuln[proyecto_fluid]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    elif "vuln[hallazgo]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    elif "vuln[id]" not in post_parms:
        return util.response([], 'Campos vacios', True)
    else:
        action = "Actualizar hallazgo, " \
            + post_parms["vuln[proyecto_fluid]"].upper() \
            + " => " + post_parms["vuln[hallazgo]"] \
            + "[" + post_parms["vuln[id]"] + "]"
    csrf = True
    if csrf == False:
        return util.response([], 'CSRF', True)
    else:
        updated = models.update_vuln_by_id(post_parms)
        if updated == {}:
            return util.response([], 'Hubo un error', True)
        else:
            if  hasattr(updated, 'text'):
                res = json.loads(updated.text)
                if "success" in res:
                    util.traceability(action, USER)
                    return util.response([], 'Success', False)
                else:
                    return util.response([], 'No se pudo actualizar formstack', True)
            else:
                return util.response([], 'No se pudo actualizar formstack', True)

@csrf_exempt
def delete_vuln(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    post_parms = request.POST.dict()
    csrf = True
    for i in post_parms:
        print i
    if csrf is False:
        return util.response([], 'CSRF', True)
    else:
        action = "Envio de campos vacios"
        if "vuln[hallazgo]" not in post_parms:
            return util.response([], 'Campos vacios', True)
        elif "vuln[proyecto_fluid]" not in post_parms:
            return util.response([], 'Campos vacios', True)
        elif "vuln[justificacion]" not in post_parms:
            return util.response([], 'Campos vacios', True)
        elif "vuln[id]" not in post_parms:
            return util.response([], 'Campos vacios', True)
        else:
            action = "Eliminar hallazgo, " \
                + post_parms["vuln[justificacion]"] \
                + " PROYECTO " + post_parms["vuln[proyecto_fluid]"].upper() \
                + " => " + post_parms["vuln[hallazgo]"] \
                + "[" + post_parms["vuln[id]"] + "]"       
        res = models.delete_vuln_by_id(post_parms["vuln[id]"])
        if res:
            util.traceability(action, USER)
            return util.response([], 'Eliminado correctamente!', False)
        else:
            return util.response([], 'No se pudo actualizar formstack', False)
