# -*- coding: utf-8 -*-
""" Vistas y servicios para FluidIntegrates """

from __future__ import absolute_import
import os
import sys
import re
import pytz
import rollbar
import boto3
import csv
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from botocore.exceptions import ClientError
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# pylint: disable=E0402
from . import util
from .decorators import authenticate, authorize
from .techdoc.IT import ITReport
from .dto.finding import FindingDTO
from .dto.closing import ClosingDTO
from .dto.project import ProjectDTO
from .dto.eventuality import EventualityDTO
from .documentator.pdf import CreatorPDF
from .documentator.secure_pdf import SecurePDF
# pylint: disable=E0402
from .mailer import send_mail_delete_finding
from .mailer import send_mail_remediate_finding
from .mailer import send_mail_new_comment
from .mailer import send_mail_reply_comment
from .mailer import send_mail_verified_finding
from .services import has_access_to_project
from .dao import integrates_dao
from .api.drive import DriveAPI
from .api.formstack import FormstackAPI
from magic import Magic
from datetime import datetime
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY

client_s3 = boto3.client('s3',
                            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = "fluidintegrates.fluidattacks.com"

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

@never_cache
@authenticate
@authorize(['analyst'])
def forms(request):
    "Vista de formularios para analistas"
    return render(request, "forms.html")

@csrf_exempt
@never_cache
@authenticate
def registration(request):
    "Vista de registro para usuarios autenticados"
    try:
        parameters = {
            'username': request.session["username"],
            'is_registered': request.session["registered"],
        }
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
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
            'company': request.session["company"],
            'last_login': request.session["last_login"],
        }
        integrates_dao.update_user_login_dao(request.session["username"])
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return redirect('/error500')
    return render(request, "dashboard.html", parameters)


@csrf_exempt
@authenticate
def logout(request):
    "Cierra la sesion activa de un usuario"

    HttpResponse("<script>Intercom('shutdown');</script>")
    try:
        del(request.session["username"])
        del(request.session["company"])
        del(request.session["role"])
        del(request.session["registered"])
    except KeyError:
        pass
    return redirect("/index")

#pylint: disable=too-many-branches
#pylint: disable=too-many-locals
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def project_to_xls(request, lang, project):
    "Crea el reporte tecnico"
    findings = []
    detail = {
        "content_type": "application/vnd.openxmlformats\
                        -officedocument.spreadsheetml.sheet",
        "content_disposition": "inline;filename=:project.xlsx",
        "path": "/usr/src/app/app/autodoc/results/:project_:username.xlsx"
    }
    username = request.session['username'].split("@")[0]
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(request.session['username'], project):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response([], 'Access denied', True)
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    for reqset in FormstackAPI().get_findings(project)["submissions"]:
        findings.append(catch_finding(request, reqset["id"]))
    data = util.ord_asc_by_criticidad(findings)
    it_report = ITReport(project, data, username)
    with open(it_report.result_filename, 'r') as document:
        response = HttpResponse(document.read(),
                                content_type=detail["content_type"])
        file_name = detail["content_disposition"]
        file_name = file_name.replace(":project", project)
        response['Content-Disposition'] = file_name
    return response

def validation_project_to_pdf(request, lang, project, doctype):
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(request.session['username'], project):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response([], 'Access denied', True)
    if lang not in ["es", "en"]:
        rollbar.report_message('Error: Unsupported language', 'error', request)
        return util.response([], 'Unsupported language', True)
    if doctype not in ["tech", "executive", "presentation"]:
        rollbar.report_message('Error: Unsupported doctype', 'error', request)
        return util.response([], 'Unsupported doctype', True)

#pylint: disable=too-many-branches
#pylint: disable=too-many-locals
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def project_to_pdf(request, lang, project, doctype):
    "Exporta un hallazgo a PDF"
    findings = []
    user = request.session['username'].split("@")[0]
    validator = validation_project_to_pdf(request, lang, project, doctype)
    if validator is not None:
        return validator
    for reqset in FormstackAPI().get_findings(project)["submissions"]:
        findings.append(catch_finding(request, reqset["id"]))
    pdf_maker = CreatorPDF(lang, doctype)
    secure_pdf = SecurePDF()
    findings = util.ord_asc_by_criticidad(findings)
    report_filename = ""
    for finding in findings:
        key_list = key_existing_list(finding['id'])
        field_list = [FindingDTO().DOC_ACHV1, FindingDTO().DOC_ACHV2, \
                    FindingDTO().DOC_ACHV3, FindingDTO().DOC_ACHV4, \
                    FindingDTO().DOC_ACHV5]
        evidence_set = util.get_evidence_set_s3(finding, key_list, field_list)
        if evidence_set:
            finding["evidence_set"] = evidence_set
            for evidence in evidence_set:
                client_s3.download_file(bucket_s3, \
                                        finding['id'] + "/" + evidence["id"], \
                                        "/usr/src/app/app/documentator/images/" + evidence["id"])
                evidence['name'] = "image::../images/"+evidence["id"]+'[align="center"]'
        else:
            evidence_set = util.get_evidence_set(finding)
            finding["evidence_set"] = evidence_set
            for evidence in evidence_set:
                DriveAPI().download_images(evidence["id"])
                evidence["name"] = "image::../images/"+evidence["id"]+'.png[align="center"]'
    if doctype == "tech":
        pdf_maker.tech(findings, project, user)
        report_filename = secure_pdf.create_full(user, pdf_maker.out_name)
    elif doctype == "executive":
        return HttpResponse("Reporte deshabilitado", content_type="text/html")
    else:
        project_info = get_project_info(project)
        mapa_id = util.drive_url_filter(project_info["mapa_hallazgos"])
        project_info["mapa_hallazgos"] = "image::../images/"+mapa_id+'.png[align="center"]'
        DriveAPI().download_images(mapa_id)
        nivel_sec = project_info["nivel_seguridad"].split(" ")[0]
        if not util.is_numeric(nivel_sec):
            return HttpResponse("Parametrizacion incorrecta", content_type="text/html")
        nivel_sec = int(nivel_sec)
        if nivel_sec < 0 or nivel_sec > 6:
            return HttpResponse("Parametrizacion incorrecta", content_type="text/html")
        project_info["nivel_seguridad"] = "image::../resources/presentation_theme/nivelsec"+str(nivel_sec)+'.png[align="center"]'
        print project_info
        if not project_info:
            return HttpResponse("Documentacion incompleta", content_type="text/html")
        pdf_maker.presentation(findings, project, project_info, user)
        #secure_pdf = SecurePDF()
        #report_filename = secure_pdf.create_only_pass(user, pdf_maker.out_name)
        report_filename = pdf_maker.RESULT_DIR + pdf_maker.out_name
    if not os.path.isfile(report_filename):
        rollbar.report_message('Error: Documentation has not been generated', 'error', request)
        raise HttpResponse('Documentation has not been generated :(', content_type="text/html")
    with open(report_filename, 'r') as document:
        response = HttpResponse(document.read(),
                                content_type="application/pdf")
        response['Content-Disposition'] = \
            "inline;filename=:id.pdf".replace(":id", user + "_" + project)
    return response

#pylint: disable-msg=R0913
@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def check_pdf(request, project):
    username = request.session['username']
    if not util.is_name(project):
        rollbar.report_message('Error: Name error in project', 'error', request)
        return util.response([], 'Name error', True)
    if not has_access_to_project(username, project):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response([], 'Access denied', True)
    reqset = get_project_info(project)
    if reqset:
        return util.response({"enable": True}, 'Success', False)
    return util.response({"enable": False}, 'Success', False)

def get_project_info(project):
    reqset = FormstackAPI().get_project_info(project)["submissions"]
    if reqset:
        submission_id = reqset[-1]["id"]
        submission = FormstackAPI().get_submission(submission_id)
        return ProjectDTO().parse(submission)
    return []

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_eventualities(request):
    "Obtiene las eventualidades con el nombre del proyecto."
    project = request.GET.get('project', None)
    category = request.GET.get('category', None)
    username = request.session['username']
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    if not has_access_to_project(username, project):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response(dataset, 'Access to project denied', True)
    if project is None:
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response(dataset, 'Empty fields in project', True)
    if category == "Name":
        submissions = api.get_eventualities(project)
        frmset = submissions["submissions"]
        for row in frmset:
            submission = api.get_submission(row["id"])
            evtset = evt_dto.parse(row["id"], submission)
            if evtset['proyecto_fluid'].lower() == project.lower():
                dataset.append(evtset)
        return util.response(dataset, 'Success', False)
    elif category == "ID":
        # Only fluid can filter by id
        if "@fluidattacks.com" not in username:
            rollbar.report_message('Error: Access to project denied', 'error', request)
            return util.response(dataset, 'Access to project denied', True)
        if not project.isdigit():
            rollbar.report_message('Error: ID is not a number', 'error', request)
            return util.response(dataset, 'ID is not a number', True)
        submission = api.get_submission(project)
        if 'error' in submission:
            return util.response(dataset, 'Event does not exist', True)
        evtset = evt_dto.parse(project, submission)
        dataset.append(evtset)
        return util.response(dataset, 'Success', False)
    else:
        rollbar.report_message('Error: An error occurred getting events', 'error', request)
        return util.response(dataset, 'Not actions', True)

@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst', 'customer'])
def get_finding(request):
    submission_id = request.POST.get('id', "")
    finding = catch_finding(request, submission_id)
    if finding:
        return util.response(finding, 'Success', False)
    rollbar.report_message('Error: An error occurred getting finding', 'error', request)
    return util.response([], 'Wrong', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
# pylint: disable=R0912
# pylint: disable=R0914
def get_findings(request):
    """Captura y procesa el nombre de un proyecto para devolver
    los hallazgos."""
    project = request.GET.get('project', "")
    username = request.session['username']
    api = FormstackAPI()
    findings = []
    if project.strip() == "":
        rollbar.report_message('Error: Empty fields in project', 'error', request)
        return util.response([], 'Empty fields', True)
    if not has_access_to_project(username, project):
        rollbar.report_message('Error: Access to project denied', 'error', request)
        return util.response([], 'Access denied', True)
    finreqset = api.get_findings(project)["submissions"]
    for submission_id in finreqset:
        finding = catch_finding(request, submission_id["id"])
        if finding['vulnerabilidad'].lower() == 'masked':
            rollbar.report_message('Warning: Project masked', 'warning', request)
            return util.response([], 'Project masked', True)
        if finding['proyecto_fluid'].lower() == project.lower():
            findings.append(finding)
    import json
    with open("/tmp/"+project+".txt", "w") as f:
        f.write(json.dumps(findings))
    return util.response(findings, 'Success', False)

def catch_finding(request, submission_id):
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    username = request.session['username']
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        finding = fin_dto.parse(
            submission_id,
            api.get_submission(submission_id),
            request
        )
        if not has_access_to_project(username, finding['proyecto_fluid']):
            rollbar.report_message('Error: Access to project denied', 'error', request)
            return None
        else:
            closingreqset = api.get_closings_by_id(submission_id)["submissions"]
            findingcloseset = []
            for closingreq in closingreqset:
                closingset = cls_dto.parse(api.get_submission(closingreq["id"]))
                findingcloseset.append(closingset)
                #El ultimo es el ultimo ciclo de cierre
                state = closingset
            finding["estado"] = state["estado"]
            finding["cierres"] = findingcloseset
            finding['cardinalidad_total'] = finding['cardinalidad']
            if 'abiertas' in state:
                finding['cardinalidad'] = state['abiertas']
            if 'abiertas_cuales' in state:
                finding['donde'] = state['abiertas_cuales']
            else:
                if state['estado'] == 'Cerrado':
                    finding['donde'] = '-'
            if 'cerradas_cuales' in state:
                finding['cerradas'] = state['cerradas_cuales']
            if state['estado'] == 'Cerrado':
                finding['donde'] = '-'
                finding['edad'] = '-'
            else:
                tzn = pytz.timezone('America/Bogota')
                finding_date = datetime.strptime(
                    finding["timestamp"].split(" ")[0],
                    '%Y-%m-%d'
                )
                finding_date = finding_date.replace(tzinfo=tzn).date()
                final_date = (datetime.now(tz=tzn).date() - finding_date)
                finding['edad'] = ":n".replace(":n", str(final_date.days))
            return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error', request)
        return None

def finding_vulnerabilities(submission_id):
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    cls_dto = ClosingDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        finding = fin_dto.parse_vulns_by_id(
            submission_id,
            api.get_submission(submission_id)
        )
        closingreqset = api.get_closings_by_id(submission_id)["submissions"]
        findingcloseset = []
        for closingreq in closingreqset:
            closingset = cls_dto.parse(api.get_submission(closingreq["id"]))
            findingcloseset.append(closingset)
            state = closingset
        finding["estado"] = state["estado"]
        finding["cierres"] = findingcloseset
        finding['cardinalidad_total'] = finding['cardinalidad']
        if 'abiertas' in state:
            finding['cardinalidad'] = state['abiertas']
        else:
            if state['estado'] == 'Cerrado':
                finding['donde'] = '-'
        if state['estado'] == 'Cerrado':
            finding['donde'] = '-'
            finding['edad'] = '-'
        else:
            tzn = pytz.timezone('America/Bogota')
            finding_date = datetime.strptime(
                finding["timestamp"].split(" ")[0],
                '%Y-%m-%d'
            )
            finding_date = finding_date.replace(tzinfo=tzn).date()
            final_date = (datetime.now(tz=tzn).date() - finding_date)
            finding['edad'] = ":n".replace(":n", str(final_date.days))
        return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error')
        return None

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_evidences(request):
    finding_id = request.GET.get('id', None)
    resp = integrates_dao.get_finding_dynamo(int(finding_id))
    return util.response(resp, 'Success', False)

@never_cache
@csrf_exempt
@authorize(['analyst', 'customer'])
def get_evidence(request, findingid, fileid):
    if fileid is None:
        rollbar.report_message('Error: Missing evidence image ID', 'error', request)
        return HttpResponse("Error - Unsent image ID", content_type="text/html")
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.png': '.tmp', '.gif': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            mime = Magic(mime=True)
            mime_type = mime.from_file(localtmp)
            if mime_type == "image/png":
                with open(localtmp, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="image/png")
            elif mime_type == "image/gif":
                with open(localtmp, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="image/gif")
            os.unlink(localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to evidence denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid evidence image ID format', 'error', request)
            return HttpResponse("Error - ID with wrong format", content_type="text/html")
        drive_api = DriveAPI(fileid)
        # pylint: disable=W0622
        if not drive_api.FILE:
            rollbar.report_message('Error: Unable to download the evidence image', 'error', request)
            return HttpResponse("Error - Unable to download the image", content_type="text/html")
        else:
            filename = "/tmp/:id.tmp".replace(":id", fileid)
            mime = Magic(mime=True)
            mime_type = mime.from_file(filename)
            if mime_type == "image/png":
                with open(filename, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="image/png")
            elif mime_type == "image/gif":
                with open(filename, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="image/gif")
            os.unlink(filename)

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

@never_cache
@csrf_exempt
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_evidences_files(request):
    parameters = request.POST.dict()
    upload = request.FILES.get("document", "")
    migrate_all_files(parameters, request)
    mime = Magic(mime=True)
    if isinstance(upload, TemporaryUploadedFile):
        mime_type = mime.from_file(upload.temporary_file_path())
    elif isinstance(upload, InMemoryUploadedFile):
        mime_type = mime.from_buffer(upload.file.getvalue())
    fieldNum = FindingDTO()
    fieldname = [['animacion', fieldNum.ANIMATION], ['explotacion', fieldNum.EXPLOTATION], \
                ['ruta_evidencia_1', fieldNum.DOC_ACHV1], ['ruta_evidencia_2', fieldNum.DOC_ACHV2], \
                ['ruta_evidencia_3', fieldNum.DOC_ACHV3], ['ruta_evidencia_4', fieldNum.DOC_ACHV4], \
                ['ruta_evidencia_5', fieldNum.DOC_ACHV5], ['exploit', fieldNum.EXPLOIT], \
                ['registros_archivo', fieldNum.REG_FILE]]
    if mime_type == "image/gif" and parameters["id"] == '0':
        if upload.size > 10485760:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "image/png" and parameters["id"] == '1':
        if upload.size > 2097152:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "image/png" and parameters["id"] in ['2', '3', '4', '5', '6']:
        if upload.size > 2097152:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'Image exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif (mime_type == "text/x-python" or mime_type == "text/x-c" \
                or mime_type == "text/plain" or mime_type == "text/html") \
                    and parameters["id"] == '7':
        if upload.size > 1048576:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'File exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    elif mime_type == "text/plain" and parameters["id"] == '8':
        if upload.size > 1048576:
            rollbar.report_message('Error - File exceeds the size limits', 'error', request)
            return util.response([], 'File exceeds the size limits', True)
        updated = update_file_to_s3(parameters, fieldname[int(parameters["id"])][1], fieldname[int(parameters["id"])][0], upload)
        return util.response([], "sended" , updated)
    rollbar.report_message('Error - Extension not allowed', 'error', request)
    return util.response([], 'Extension not allowed', True)

def key_existing_list(key):
    """return the key's list if it exist, else list empty"""
    response = client_s3.list_objects_v2(
        Bucket=bucket_s3,
        Prefix=key,
    )
    key_list = []
    for obj in response.get('Contents', []):
        key_list.append(obj['Key'])
    return key_list

def send_file_to_s3(filename, parameters, field, fieldname, ext):
    fileurl = parameters['findingId'] + '/' + parameters['url']
    fileroute = "/tmp/:id.tmp".replace(":id", filename)
    namecomplete = fileurl + "-" + field + "-" + filename + ext
    if os.path.exists(fileroute):
        with open(fileroute, "r") as file_obj:
            try:
                client_s3.upload_fileobj(file_obj, bucket_s3, namecomplete)
            except ClientError:
                rollbar.report_exc_info()
                integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "es_" + fieldname, False)
                return False
        resp = integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "es_" + fieldname, True)
        if not resp:
            integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "es_" + fieldname, False)
        os.unlink(fileroute)
        return resp
    else:
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, namecomplete.split("/")[1], "es_" + fieldname, False)
        return False

def update_file_to_s3(parameters, field, fieldname, upload):
    fileurl = parameters['findingId'] + '/' + parameters['url']
    key_val = fileurl + "-" + field
    key_list = key_existing_list(key_val)
    if key_list:
        for k in key_list:
            client_s3.delete_object(Bucket=bucket_s3, Key=k)
    filename = fileurl + "-" + field + "-" + upload.name
    try:
        client_s3.upload_fileobj(upload.file, bucket_s3, filename)
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, filename.split("/")[1], "es_" + fieldname, True)
        return False
    except ClientError:
        rollbar.report_exc_info()
        integrates_dao.add_finding_dynamo(int(parameters['findingId']), fieldname, filename.split("/")[1], "es_" + fieldname, False)
        return True

def migrate_all_files(parameters, request):
    fin_dto = FindingDTO()
    try:
        api = FormstackAPI()
        frmreq = api.get_submission(parameters['findingId'])
        finding = fin_dto.parse(parameters['findingId'], frmreq, request)
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.ANIMATION
        folder = key_existing_list(filename)
        if "animacion" in finding and parameters["id"] != '0' and not folder:
            send_file_to_s3(finding["animacion"], parameters, fin_dto.ANIMATION, "animacion", ".gif")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOTATION
        folder = key_existing_list(filename)
        if "explotacion" in finding and parameters["id"] != '1' and not folder:
            send_file_to_s3(finding["explotacion"], parameters, fin_dto.EXPLOTATION, "explotacion", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV1
        folder = key_existing_list(filename)
        if "ruta_evidencia_1" in finding and parameters["id"] != '2' and not folder:
            send_file_to_s3(finding["ruta_evidencia_1"], parameters, fin_dto.DOC_ACHV1, "ruta_evidencia_1", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV2
        folder = key_existing_list(filename)
        if "ruta_evidencia_2" in finding and parameters["id"] != '3' and not folder:
            send_file_to_s3(finding["ruta_evidencia_2"], parameters, fin_dto.DOC_ACHV2, "ruta_evidencia_2", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV3
        folder = key_existing_list(filename)
        if "ruta_evidencia_3" in finding and parameters["id"] != '4' and not folder:
            send_file_to_s3(finding["ruta_evidencia_3"], parameters, fin_dto.DOC_ACHV3, "ruta_evidencia_3", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV4
        folder = key_existing_list(filename)
        if "ruta_evidencia_4" in finding and parameters["id"] != '5' and not folder:
            send_file_to_s3(finding["ruta_evidencia_4"], parameters, fin_dto.DOC_ACHV4, "ruta_evidencia_4", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.DOC_ACHV5
        folder = key_existing_list(filename)
        if "ruta_evidencia_5" in finding and parameters["id"] != '6' and not folder:
            send_file_to_s3(finding["ruta_evidencia_5"], parameters, fin_dto.DOC_ACHV5, "ruta_evidencia_5", ".png")
        filename =  parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.EXPLOIT
        folder = key_existing_list(filename)
        if "exploit" in finding and parameters["id"] != '7' and not folder:
            send_file_to_s3(finding["exploit"], parameters, fin_dto.EXPLOIT, "exploit", ".py")
        filename = parameters['findingId'] + "/" + parameters['url'] + "-" + fin_dto.REG_FILE
        folder = key_existing_list(filename)
        if "registros_archivo" in finding and parameters["id"] != '8' and not folder:
            send_file_to_s3(finding["registros_archivo"], parameters, fin_dto.REG_FILE, "registros_archivo", ".csv")
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_evidence_text(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_evidence_description(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating description', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_exploit(request):
    parameters = request.GET.dict()
    fileid = parameters['id']
    findingid = parameters['findingid']
    if fileid is None:
        rollbar.report_message('Error: Missing exploit ID', 'error', request)
        return HttpResponse("Error - Unsent exploit ID", content_type="text/html")
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.py': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            mime = Magic(mime=True)
            mime_type = mime.from_file(localtmp)
            if mime_type == "text/x-python" or mime_type == "text/x-c" \
                or mime_type == "text/plain" or mime_type == "text/html":
                with open(localtmp, "r") as file_obj:
                    return HttpResponse(file_obj.read(), content_type="text/plain")
            os.unlink(localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to exploit denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid exploit ID format', 'error', request)
            return HttpResponse("Error - ID with wrong format", content_type="text/html")
        drive_api = DriveAPI(fileid)
        if drive_api.FILE is None:
            rollbar.report_message('Error: Unable to download the exploit', 'error', request)
            return HttpResponse("Error - Unable to download the file", content_type="text/html")
        filename = "/tmp/:id.tmp".replace(":id", fileid)
        mime = Magic(mime=True)
        mime_type = mime.from_file(filename)
        if mime_type == "text/x-c" or mime_type == "text/x-python" or mime_type == "text/plain" \
            or mime_type == "text/html":
            with open(filename, "r") as file_obj:
                return HttpResponse(file_obj.read(), content_type="text/plain")
        os.unlink(filename)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_records(request):
    parameters = request.GET.dict()
    fileid = parameters['id']
    findingid = parameters['findingid']
    if fileid is None:
        rollbar.report_message('Error: Missing record file ID', 'error', request)
        return util.response([], 'Unsent record file ID', True)
    key_list = key_existing_list(findingid + "/" + fileid)
    if key_list:
        for k in key_list:
            start = k.find(findingid) + len(findingid)
            localfile = "/tmp" + k[start:]
            ext = {'.py': '.tmp'}
            localtmp = replace_all(localfile, ext)
            client_s3.download_file(bucket_s3, k, localtmp)
            mime = Magic(mime=True)
            mime_type = mime.from_file(localtmp)
            resp = []
            if mime_type == "text/plain":
                with open(localtmp, "r") as file_obj:
                    csvReader = csv.reader(file_obj, lineterminator="\n")
                    header = csvReader.next()
                    for row in csvReader:
                        dicTok = list_to_dict(header, row)
                        resp.append(dicTok)
                    return util.response(resp, 'Success', False)
            os.unlink(localtmp)
    else:
        if fileid not in request.session:
            rollbar.report_message('Error: Access to record file denied', 'error', request)
            return util.response([], 'Access denied', True)
        if not re.match("[a-zA-Z0-9_-]{20,}", fileid):
            rollbar.report_message('Error: Invalid record file ID format', 'error', request)
            return util.response([], 'ID with wrong format', True)
        drive_api = DriveAPI(fileid)
        if drive_api.FILE is None:
            rollbar.report_message('Error: Unable to download the record file', 'error', request)
            return util.response([], 'Unable to download the file', True)
        filename = "/tmp/:id.tmp".replace(":id", fileid)
        mime = Magic(mime=True)
        mime_type = mime.from_file(filename)
        resp = []
        if mime_type == "text/plain":
            with open(filename, "r") as file_obj:
                csvReader = csv.reader(file_obj, lineterminator="\n")
                header = csvReader.next()
                for row in csvReader:
                    dicTok = list_to_dict(header, row)
                    resp.append(dicTok)
                return util.response(resp, 'Success', False)
        os.unlink(filename)

def list_to_dict(header, li):
    dct = {}
    cont = 0
    if len(header) < len(li):
        dif  = len(li) - len(header)
        for x in range(dif): # pylint: disable=unused-variable
            header.append("")
    elif len(header) > len(li):
        dif  = len(header) - len(li)
        for x in range(dif): # pylint: disable=unused-variable
            li.append("")

    for item in li:
        if header[cont] == "":
            dct[cont] = item
        else:
            dct[header[cont]] = item
        cont += 1
    return dct

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_myevents(request):
    user = request.session["username"]
    projects = integrates_dao.get_projects_by_user(user)
    dataset = []
    evt_dto = EventualityDTO()
    api = FormstackAPI()
    for row in projects:
        project = row[0]
        submissions = api.get_eventualities(project)
        frmset = submissions["submissions"]
        for evtsub in frmset:
            submission = api.get_submission(evtsub["id"])
            evtset = evt_dto.parse(evtsub["id"], submission)
            if evtset['proyecto_fluid'].lower() == project.lower():
                if evtset['estado'] == "Pendiente":
                    dataset.append(evtset)
    return util.response(dataset, 'Success', False)


@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_myprojects(request):
    user = request.session["username"]
    data_set = integrates_dao.get_projects_by_user(user)
    json_data = []
    for row in data_set:
        json_data.append({
            "project": row[0].upper(),
            "company_project": row[1]
        })
    return util.response(json_data, 'Success', False)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_cssv2(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_cssv2(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating CSSV2', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_description(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_description(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating description', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer'])
def update_treatment(request):
    parameters = request.POST.dict()
    try:
        generic_dto = FindingDTO()
        generic_dto.create_treatment(parameters)
        generic_dto.to_formstack()
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error occurred updating treatment', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def update_eventuality(request):
    "Actualiza una eventualidad asociada a un proyecto"
    parameters = request.POST.dict()
    try:
        generic_dto = EventualityDTO()
        generic_dto.create(parameters)
        if not parameters["vuln[afectacion]"].isdigit():
            rollbar.report_message('Error: Affectation can not be a negative number', 'error', request)
            return util.response([], 'Afectacion negativa', True)
        api = FormstackAPI()
        request = api.update(generic_dto.request_id, generic_dto.data)
        if request:
            return util.response([], 'success', False)
        rollbar.report_message('Error: An error ocurred updating event', 'error', request)
        return util.response([], 'error', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def delete_finding(request):
    """Captura y procesa el id de una eventualidad para eliminarla"""
    parameters = request.POST.dict()
    username = request.session['username']
    fin_dto = FindingDTO()
    try:
        submission_id = parameters["data[id]"]
        context = fin_dto.create_delete(parameters, username, "", "")
        api = FormstackAPI()
        frmreq = api.get_submission(submission_id)
        finding = fin_dto.parse(submission_id, frmreq, request)
        context["project"] = finding["proyecto_fluid"]
        context["name_finding"] = finding["hallazgo"]
        result = api.delete_submission(submission_id)
        if result is None:
            rollbar.report_message('Error: An error ocurred deleting finding', 'error', request)
            return util.response([], 'Error', True)
        to = ["engineering@fluidattacks.com"]
        send_mail_delete_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['customer'])
def finding_solved(request):
    """ Envia un correo solicitando la revision de un hallazgo """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    remediated = integrates_dao.add_remediated_dynamo(int(parameters['data[finding_id]']), True, parameters['data[project]'], parameters['data[finding_name]'])
    rem_solution = parameters['data[justification]'].replace('\n', ' ')
    if not remediated:
        rollbar.report_message('Error: An error occurred when remediating the finding', 'error', request)
        return util.response([], 'Error', True)
    # Send email parameters
    try:
        to = [x[0] for x in recipients]
        to.append('continuous@fluidattacks.com')
        to.append('projects@fluidattacks.com')
        to.append('ralvarez@fluidattacks.com')
        context = {
           'project': parameters['data[project]'],
           'finding_name': parameters['data[finding_name]'],
           'user_mail': parameters['data[user_mail]'],
           'finding_url': parameters['data[finding_url]'],
           'finding_id': parameters['data[finding_id]'],
           'finding_vulns': parameters['data[finding_vulns]'],
           'company': request.session["company"],
           'solution': rem_solution,
            }
        send_mail_remediate_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst'])
def finding_verified(request):
    """ Envia un correo informando que el hallazgo fue verificado """
    parameters = request.POST.dict()
    recipients = integrates_dao.get_project_users(parameters['data[project]'])
    verified = integrates_dao.add_remediated_dynamo(int(parameters['data[finding_id]']), False, parameters['data[project]'], parameters['data[finding_name]'])
    if not verified:
        rollbar.report_message('Error: An error occurred when verifying the finding', 'error', request)
        return util.response([], 'Error', True)
    # Send email parameters
    try:
        to = [x[0] for x in recipients]
        to.append('continuous@fluidattacks.com')
        to.append('projects@fluidattacks.com')
        to.append('ralvarez@fluidattacks.com')
        context = {
           'project': parameters['data[project]'],
           'finding_name': parameters['data[finding_name]'],
           'user_mail': parameters['data[user_mail]'],
           'finding_url': parameters['data[finding_url]'],
           'finding_id': parameters['data[finding_id]'],
           'finding_vulns': parameters['data[finding_vulns]'],
           'company': request.session["company"],
            }
        send_mail_verified_finding(to, context)
        return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_remediated(request):
    finding_id = request.GET.get('id', "")
    remediated = integrates_dao.get_remediated_dynamo(int(finding_id))
    if remediated == []:
        return util.response({'remediated': False}, 'Success', False)
    resp = False
    for row in remediated:
        resp = row['remediated']
    return util.response({'remediated': resp}, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_comments(request):
    submission_id = request.GET.get('id', "")
    comments = integrates_dao.get_comments_dynamo(int(submission_id))
    json_data = []
    for row in comments:
        aux = row['email'] == request.session["username"]
        json_data.append({
            'id': int(row['user_id']),
            'parent': int(row['parent']),
            'created': row['created'],
            'modified': row['modified'],
            'content': row['content'],
            'fullname': row['fullname'],
            'created_by_current_user': aux,
            'email': row['email']
        })
    return util.response(json_data, 'Success', False)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer'])
def add_comment(request):
    submission_id = request.POST.get('id', "")
    data = request.POST.dict()
    data["data[created]"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["data[modified]"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    email = request.session["username"]
    data["data[fullname]"] = request.session["first_name"] + " " + request.session["last_name"]
    comment = integrates_dao.create_comment_dynamo(int(submission_id), email, data)
    if not comment:
        rollbar.report_message('Error: An error ocurred adding comment', 'error', request)
        return util.response([], 'Error', True)
    try:
        recipients = integrates_dao.get_project_users(data['data[project]'].lower())
        to = [x[0] for x in recipients]
        to.append('continuous@fluidattacks.com')
        comment_content = data['data[content]'].replace('\n', ' ')
        context = {
           'project': data['data[project]'],
           'finding_name': data['data[finding_name]'],
           'user_email': email,
           'finding_url': data['data[finding_url]'],
           'finding_id': submission_id,
           'comment': comment_content,
            }
        if data["data[remediated]"] != "true":
            if data["data[parent]"] == '0':
                send_mail_new_comment(to, context)
                return util.response([], 'Success', False)
            elif data["data[parent]"] != '0':
                send_mail_reply_comment(to, context)
                return util.response([], 'Success', False)
        else:
            return util.response([], 'Success', False)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)
        return util.response([], 'Campos vacios', True)

@never_cache
@require_http_methods(["POST"])
@authorize(['analyst', 'customer'])
def delete_comment(request):
    submission_id = request.POST.get('id', "")
    data = request.POST.dict()
    comment = integrates_dao.delete_comment_dynamo(int(submission_id), data)
    if not comment:
        rollbar.report_message('Error: An error ocurred deleting comment', 'error', request)
        return util.response([], 'Error', True)
    return util.response([], 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def total_severity(request):
    project = request.GET.get('project', "")
    toe = integrates_dao.get_toe_dynamo(project)
    return util.response(toe, 'Success', False)

@never_cache
@csrf_exempt
@require_http_methods(["GET"])
@authorize(['analyst', 'customer'])
def get_alerts(request):
    company = request.GET.get('company', None)
    project = request.GET.get('project', None)
    resp = integrates_dao.get_company_alert_dynamo(company, project)
    return util.response(resp, 'Success', False)
