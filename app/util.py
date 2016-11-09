# -*- coding: utf-8 -*-
"""
    Funciones de utilidad para FluidIntegrates
"""
import re
import os
import datetime
import json
from django.http import JsonResponse


def is_authenticated(request):
    """ Verifica si existe una sesion en el sistema"""
    if "username" in request.session:
        if request.session["username"] is None:
            return False
        return True
    return False

def response(data, message, error):
    "Crea un objeto para enviar respuestas genericas"
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return JsonResponse(response_data)

def traceability(msg, user):
    """ Funcion para llevar un log de acciones personalizadas \
        independientes de logging """
    file_obj = None
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        filename = base + "/logs/integrates.log"
        logmsg = str(datetime.datetime.now()) + "," + user+ "," + msg.encode('utf8')
        file_obj = open(filename, 'a')
        file_obj.write(logmsg.encode('utf8'))
        file_obj.close()
    except (OSError, IOError) as expt:
        print "ERROR CON EL LOG " + expt.message()

def is_name(name):
    """ Verifica que un parametro tenga el formato
        de nombre adecuado """
    valid = True
    try:
        if not name:
            raise ValueError("")
        elif name.strip() == "":
            raise ValueError("")
        elif not re.search("^[a-zA-Z0-9]+$", name):
            raise ValueError("")
    except ValueError:
        valid = False
    return valid

def is_json(data):
    """ Verifica si el parametro dado es un json """
    valid = True
    try:
        json.loads(data)
    except ValueError:
        valid = False
    except TypeError:
        valid = False
    return valid

def ord_asc_by_criticidad(data):
    """ Ordena los hallazgos por criticidad """
    for i in range(0, len(data)-1):
        for j in range(i+1, len(data)):
            firstc = float(data[i]["criticidad"])
            seconc = float(data[j]["criticidad"])
            if firstc < seconc:
                aux = data[i]
                data[i] = data[j]
                data[j] = aux
    return data

def extract_reqs(req_vect):
    """ Obtiene todos los identificadores con el formato REQ.XXXX"""
    try:
        reqs = re.findall("REQ\\.\\d{3,4}", req_vect)
        reqs = [x.replace("REQ.", "") for x in reqs]
        return "|".join(reqs)
    except ValueError:
        return ""

def extract_metric(metric_str):
    "Obtiene los valores de la cadena de texto con las \
     metricas de calificacion de formstack"
    try:
        return metric_str.split("|")[1].strip().split(":")[0].strip()
    except ValueError:
        return ""
