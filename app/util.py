# -*- coding: utf-8 -*-
"""
    Funciones de utilidad para FluidIntegrates
"""
import re
import os
import datetime
import json
from django.http import JsonResponse


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
        logmsg = str(datetime.datetime.now()) + "," + user + "," + msg
        file_obj = open(filename, 'a')
        file_obj.write(logmsg)
        file_obj.close()
    except (OSError, IOError) as expt:
        print("ERROR CON EL LOG " + expt.message())


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


def is_numeric(name):
    """ Verifica que un parametro tenga el formato
        de numero adecuado """
    valid = True
    try:
        if not name:
            raise ValueError("")
        elif name.strip() == "":
            raise ValueError("")
        elif not re.search("^[0-9]+$", name):
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

def drive_url_filter(drive):
    """ Obtiene el ID de la imagen de drive """
    if(drive.find("id=") != -1):
        new_url = drive.split("id=")[1]
        if(new_url.find("&") != -1):
            return new_url.split("&")[0]
    return drive
    