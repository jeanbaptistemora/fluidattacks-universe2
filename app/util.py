# -*- coding: utf-8 -*-
"""
    Funciones de utilidad para FluidIntegrates
"""
import re
import os
import datetime
import json
import hmac
import hashlib
import rollbar
from magic import Magic
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
        rollbar.report_message("ERROR WITH LOG " + expt.message(), 'error')
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


def get_hmac(request):
    result = hmac.new(
                'xuk7Un2cie5Aenej8joo2Xaefui1ai',
                request.user.email,
                digestmod=hashlib.sha256)
    return result.hexdigest()

def get_evidence_set(finding):
    evidence_set = []
    if "ruta_evidencia_1" in finding and \
        "desc_evidencia_1" in finding:
        evidence_set.append({
            "id": finding["ruta_evidencia_1"],
            "explicacion": finding["desc_evidencia_1"].capitalize()
        })
    if "ruta_evidencia_2" in finding and \
        "desc_evidencia_2" in finding:
        evidence_set.append({
            "id": finding["ruta_evidencia_2"],
            "explicacion": finding["desc_evidencia_2"].capitalize()
        })
    if "ruta_evidencia_3" in finding and \
        "desc_evidencia_3" in finding:
        evidence_set.append({
            "id": finding["ruta_evidencia_3"],
            "explicacion": finding["desc_evidencia_3"].capitalize()
        })
    if "ruta_evidencia_4" in finding and \
        "desc_evidencia_4" in finding:
        evidence_set.append({
            "id": finding["ruta_evidencia_4"],
            "explicacion": finding["desc_evidencia_4"].capitalize()
        })
    if "ruta_evidencia_5" in finding and \
        "desc_evidencia_5" in finding:
        evidence_set.append({
            "id": finding["ruta_evidencia_5"],
            "explicacion": finding["desc_evidencia_5"].capitalize()
        })
    return evidence_set

def get_evidence_set_s3(finding, key_list, field_list):
    evidence_set = []
    for k in key_list:
        ruta_evidencia_1 = finding['id'] + "/" + finding['proyecto_fluid'].lower() \
                            + "-" + finding['id'] + "-" + field_list[0]
        if "desc_evidencia_1" in finding and \
            ruta_evidencia_1 in k:
            evidence_set.append({
                "id": k.split("/")[1],
                "explicacion": finding["desc_evidencia_1"].capitalize()
            })
        ruta_evidencia_2 = finding['id'] + "/" + finding['proyecto_fluid'].lower() \
                            + "-" + finding['id'] + "-" + field_list[1]
        if "desc_evidencia_2" in finding and \
            ruta_evidencia_2 in k:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explicacion": finding["desc_evidencia_2"].capitalize()
            })
        ruta_evidencia_3 = finding['id'] + "/" + finding['proyecto_fluid'].lower() \
                            + "-" + finding['id'] + "-" + field_list[2]
        if "desc_evidencia_3" in finding and \
            ruta_evidencia_3 in finding:
            evidence_set.append({
                "id": k.split("/")[1],
                "explicacion": finding["desc_evidencia_3"].capitalize()
            })
        ruta_evidencia_4 = finding['id'] + "/" + finding['proyecto_fluid'].lower() \
                            + "-" + finding['id'] + "-" + field_list[3]
        if "desc_evidencia_4" in finding and \
            ruta_evidencia_4 in finding:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explicacion": finding["desc_evidencia_4"].capitalize()
            })
        ruta_evidencia_5 = finding['id'] + "/" + finding['proyecto_fluid'].lower() \
                            + "-" + finding['id'] + "-" + field_list[4]
        if "desc_evidencia_5" in finding and \
            ruta_evidencia_5 in finding:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explicacion": finding["desc_evidencia_5"].capitalize()
            })
    return evidence_set

def get_ext_filename(drive_id):
    filename = "/tmp/img_:id".replace(":id", drive_id)
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    if mime_type == "image/png":
        return filename+".png"
    elif mime_type == "image/jpeg":
        return filename+".jgp"
    elif mime_type == "image/gif":
        return filename+".gif"