from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.template import Context, loader
from . import models, response
import os
import json

def index(request):
    c = {}
    return render(request, "index.html", c)

@csrf_exempt
def dashboard(request):
    c = {}
    return render(request, "dashboard.html", c)

#@requires_csrf_token
@csrf_exempt
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not username or not password:
    	return JsonResponse(response.object([],'Empty fields',True))
    else:
        try:
            result = models.one_login_auth(username, password)  
            if result["status"]["type"] == "success":
                request.session['username'] = username
                return JsonResponse(response.object([],'Success',False))
            else:
                return JsonResponse(response.object([],'Wrong! Username/Password',True))
        except:
            return JsonResponse(response.object([],'Connection Error',True))

@csrf_exempt
def get_vuln_by_name(request):
    project = request.GET.get('project', None)
    if not project:
        return JsonResponse(response.object([],'Empty fields',True))
    else:
        if project.strip() == "":
        	    return JsonResponse(response.object([],'Empty fields',True))
        else:
            result = models.get_vuln_by_name(project)["submissions"]
            if len(result) == 0:
                return JsonResponse(response.object([],'Project doesn\'t exist',True))
            else:
                ids = []
                vulns = []
                for i in result: 
                    ids.append(i["id"])
                for id in ids:
                    vuln = models.get_vuln_by_submission_id(id)
                    vulns.append(vuln)
                return JsonResponse(response.object(vulns,'Success',False))

@csrf_exempt
def get_vuln_by_date(request):
    from_date = request.GET.get('from', None)
    to_date = request.GET.get('tp', None)

    if not from_date or not to_date:
        return JsonResponse(response.object([],'Empty fields',True))
    else:
        if from_date.strip() == "" or to_date.strip() == "" :
        	    return JsonResponse(response.object([],'Empty fields',True))
        else:
            return HttpResponse("TEST2")

@csrf_exempt
def get_evnt_by_name(request):
    project = request.GET.get('project', None)
    if not project:
        return JsonResponse(response.object([],'Empty fields',True))
    else:
        if project.strip() == "":
        	    return JsonResponse(response.object([],'Empty fields',True))
        else:
            return HttpResponse("TEST3")
        
@csrf_exempt
def update_vuln(request):
    req = request.POST.dict();
    res = models.update_vuln_by_id(req)
    counter = 10
    while(res == None and counter != 0):
        res = models.update_vuln_by_id(req)
        counter -= 1
    if(res == None):
        return JsonResponse(response.object([],'No hay conexion con formstack',True))
    else:
        res = json.loads(res.text)
        if "success" in res:
            return JsonResponse(response.object([],'Success',False))
        else:
            return JsonResponse(response.object([],'No se pudo actualizar formstack',True))

@csrf_exempt
def delete_vuln(request):
    req = request.POST.dict();
    req = request.POST.dict();
    res = models.delete_vuln_by_id(req)
    return JsonResponse(response.object([],'No se pudo actualizar formstack',False))