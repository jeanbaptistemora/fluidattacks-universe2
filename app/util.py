# -*- coding: utf-8 -*-
""" FluidIntegrates auxiliar functions. """
import logging
import logging.config
import re
import os
import datetime
import json
import hmac
import hashlib
import rollbar
import pytz
from magic import Magic
from django.conf import settings
from django.http import JsonResponse

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

def response(data, message, error):
    """ Create an object to send generic answers """
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return JsonResponse(response_data)


def traceability(msg, user):
    """ Function to create a customizable actions log
        independent of the traditional log. """
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
    """ Verify that a parameter has the appropriate name format. """
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
    """ Verify that a parameter has the appropriate number format. """
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
    """ Check if the given parameter is a json """
    valid = True
    try:
        json.loads(data)
    except ValueError:
        valid = False
    except TypeError:
        valid = False
    return valid


def ord_asc_by_criticidad(data):
    """ Sort the findings by criticality """
    for i in range(0, len(data)-1):
        for j in range(i+1, len(data)):
            firstc = float(data[i]["criticity"])
            seconc = float(data[j]["criticity"])
            if firstc < seconc:
                aux = data[i]
                data[i] = data[j]
                data[j] = aux
    return data


def drive_url_filter(drive):
    """ Gets the ID of an image stored on Google Drive """
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
    if "evidence_route_1" in finding and \
        "evidence_description_1" in finding:
        evidence_set.append({
            "id": finding["evidence_route_1"],
            "explanation": finding["evidence_description_1"].capitalize()
        })
    if "evidence_route_2" in finding and \
        "evidence_description_2" in finding:
        evidence_set.append({
            "id": finding["evidence_route_2"],
            "explanation": finding["evidence_description_2"].capitalize()
        })
    if "evidence_route_3" in finding and \
        "evidence_description_3" in finding:
        evidence_set.append({
            "id": finding["evidence_route_3"],
            "explanation": finding["evidence_description_3"].capitalize()
        })
    if "evidence_route_4" in finding and \
        "evidence_description_4" in finding:
        evidence_set.append({
            "id": finding["evidence_route_4"],
            "explanation": finding["evidence_description_4"].capitalize()
        })
    if "evidence_route_5" in finding and \
        "evidence_description_5" in finding:
        evidence_set.append({
            "id": finding["evidence_route_5"],
            "explanation": finding["evidence_description_5"].capitalize()
        })
    return evidence_set

def get_evidence_set_s3(finding, key_list, field_list):
    evidence_set = []
    for k in key_list:
        evidence_route_1 = finding['id'] + "/" + finding['fluidProject'].lower() \
                            + "-" + finding['id'] + "-" + field_list[0]
        if "evidence_description_1" in finding and \
            evidence_route_1 in k:
            evidence_set.append({
                "id": k.split("/")[1],
                "explanation": finding["evidence_description_1"].capitalize()
            })
        evidence_route_2 = finding['id'] + "/" + finding['fluidProject'].lower() \
                            + "-" + finding['id'] + "-" + field_list[1]
        if "evidence_description_2" in finding and \
            evidence_route_2 in k:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explanation": finding["evidence_description_2"].capitalize()
            })
        evidence_route_3 = finding['id'] + "/" + finding['fluidProject'].lower() \
                            + "-" + finding['id'] + "-" + field_list[2]
        if "evidence_description_3" in finding and \
            evidence_route_3 in finding:
            evidence_set.append({
                "id": k.split("/")[1],
                "explanation": finding["evidence_description_3"].capitalize()
            })
        evidence_route_4 = finding['id'] + "/" + finding['fluidProject'].lower() \
                            + "-" + finding['id'] + "-" + field_list[3]
        if "evidence_description_4" in finding and \
            evidence_route_4 in finding:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explanation": finding["evidence_description_4"].capitalize()
            })
        evidence_route_5 = finding['id'] + "/" + finding['fluidProject'].lower() \
                            + "-" + finding['id'] + "-" + field_list[4]
        if "evidence_description_5" in finding and \
            evidence_route_5 in finding:
            evidence_set.append({
                "id":  k.split("/")[1],
                "explanation": finding["evidence_description_5"].capitalize()
            })
    return evidence_set

def get_ext_filename(drive_id):
    filename = "/tmp/img_:id".replace(":id", drive_id)
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    if mime_type == "image/png":
        return filename+".png"
    elif mime_type == "image/jpeg":
        return filename+".jpg"
    elif mime_type == "image/gif":
        return filename+".gif"

def user_email_filter(emails, actualUser):
    if "@fluidattacks.com" in actualUser:
        finalUsers = emails
    else:
        for user in emails:
            if "@fluidattacks.com" in user:
                emails.remove(user)
        finalUsers = emails
    return finalUsers

def assert_file_mime(filename, allowed_mimes):
    mime = Magic(mime=True)
    mime_type = mime.from_file(filename)
    return mime_type in allowed_mimes

def validate_release_date(finding):
    """Validate if a release has a valid date."""
    if 'releaseDate' in finding:
        tzn = pytz.timezone('America/Bogota')
        today_day = datetime.datetime.now(tz=tzn).date()
        finding_last_vuln = datetime.datetime.strptime(
            finding["releaseDate"].split(" ")[0],
            '%Y-%m-%d'
        )
        finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
        result = finding_last_vuln <= today_day
    else:
        result = False
    return result

def validate_session_time(project, request):
    """Validate if project data is in session."""
    if ("projects" in request.session and
            project in request.session["projects"] and
            project + "_date" in request.session["projects"]):
        project_time = datetime.datetime.strptime(
            request.session["projects"][project + "_date"],
            "%Y-%m-%d %H:%M:%S.%f"
        )
        time_delta = (datetime.datetime.today() - project_time).total_seconds()
        result = time_delta < 600
    else:
        result = False
    return result

def cloudwatch_log(request, msg):
    info = [request.session["username"], request.session["company"]]
    for parameter in ["project", "findingid"]:
        if parameter in request.POST.dict():
            info.append(request.POST.dict()[parameter])
        elif parameter in request.GET.dict():
            info.append(request.GET.dict()[parameter])
    info.append(msg)
    logger.info(":".join(info))
