from __future__ import unicode_literals

from django.db import models
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
from time import sleep
requests.adapters.DEFAULT_RETRIES = 10

config = {
    'headers':{
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    },
    'formstack': {
        'token': 'aefb128ba610da7e8d9e0b6ff86d9d7a',
        'forms':{
            'get_vuln_by_name':{
                'url': 'https://www.formstack.com/api/v2/form/1998500/submission.json',
                'fields': {
                    'name' : '32201732'
                }
            },
            'get_submission_by_id':{
                'url' : 'https://www.formstack.com/api/v2/submission/:id.json'
            },
            'create_delete_registry':{
                'url': 'https://www.formstack.com/api/v2/form/2388563/submission.json'
            }
        },
        'fields':{
            'project':{
                'analista': "32201744",
                'lider': "38193323",
                'interesado': "38392409",
                'proyecto_fluid': "32201732",
                'proyecto_cliente': "38209122",
                'tipo_prueba': "38254692",
                'contexto': "38404474",
                'nivel': "38392454"
            },
            'vuln':{
                'hallazgo': "32201810",
                'codigo_cliente': "38193365",
                'probabilidad': "38193660",
                'severidad': "38193659",
                'nivel_riesgo': "38194645",
                'cardinalidad': "38255025",
                'donde': "38193357",
                'criticidad': "38529256",
                'vulnerabilidad': "32202728",
                'amenaza': "38193361",
                'componente_aplicativo': "38209122",
                'tipo_prueba': "38254692",
                'riesgo': "38193362",
                'requisitos': "38254586",
                'solucion_efecto': "38619077",
                'tipo': "38392454",
            },
            'delete':{
                'analista':'43112177',
                'id':'43112343',
                'hallazgo':'43112522',
                'proyecto':'43112517',
                'justificacion':'43112373' 
            }
        }
    },
    'onelogin': {
        'url': 'https://api.onelogin.com/api/v3/saml/assertion',
        'api_key': 'e5996692a9bf56a66f8d4542948c47ac7913c505',
        'app_id': '476874'
    }
}
def parse_formstack_vuln_req(formstack_vuln,id):
    vuln = dict()
    configCtx = config["formstack"]["fields"]["vuln"]
    configPrj = config["formstack"]["fields"]["project"]
    vuln["id"] = id
    for i in formstack_vuln:
        #DETALLES VULNERABILIDAD
        if i["field"] == configCtx["hallazgo"]:
            vuln["hallazgo"] = i["value"]
        if i["field"] == configCtx["codigo_cliente"]:
            vuln["codigo_cliente"] = i["value"]
        if i["field"] == configCtx["probabilidad"]:
            vuln["probabilidad"] = i["value"]
        if i["field"] == configCtx["severidad"]:
            vuln["severidad"] = i["value"]
        if i["field"] == configCtx["nivel_riesgo"]:
            vuln["nivel_riesgo"] = i["value"]
        if i["field"] == configCtx["cardinalidad"]:
            vuln["cardinalidad"] = i["value"]
        if i["field"] == configCtx["donde"]:
            vuln["donde"] = i["value"]
        if i["field"] == configCtx["criticidad"]:
            vuln["criticidad"] = i["value"]
        if i["field"] == configCtx["vulnerabilidad"]:
            vuln["vulnerabilidad"] = i["value"]
        if i["field"] == configCtx["amenaza"]:
            vuln["amenaza"] = i["value"]
        if i["field"] == configCtx["componente_aplicativo"]:
            vuln["componente_aplicativo"] = i["value"]
        if i["field"] == configCtx["tipo_prueba"]:
            vuln["tipo_prueba"] = i["value"]
        if i["field"] == configCtx["riesgo"]:
            vuln["riesgo"] = i["value"]
        if i["field"] == configCtx["requisitos"]:
            vuln["requisitos"] = i["value"]
        if i["field"] == configCtx["solucion_efecto"]:
            vuln["solucion_efecto"] = i["value"]
        if i["field"] == configCtx["tipo"]:
            vuln["tipo"] = i["value"]
        #DETALLES PROYECTO
        if i["field"] == configPrj["analista"]:
            vuln["analista"] = i["value"]
        if i["field"] == configPrj["lider"]:
            vuln["lider"] = i["value"]
        if i["field"] == configPrj["interesado"]:
            vuln["interesado"] = i["value"]
        if i["field"] == configPrj["proyecto_fluid"]:
            vuln["proyecto_fluid"] = i["value"]
        if i["field"] == configPrj["proyecto_cliente"]:
            vuln["proyecto_cliente"] = i["value"]
        if i["field"] == configPrj["contexto"]:
            vuln["contexto"] = i["value"]
        if i["field"] == configPrj["nivel"]:
            vuln["nivel"] = i["value"]
    return vuln
        

def get_vuln_by_name (project):
    url = config["formstack"]["forms"]["get_vuln_by_name"]["url"]
    data = {
        'oauth_token': config["formstack"]["token"],
        'search_field_1': config["formstack"]["forms"]["get_vuln_by_name"]["fields"]["name"],
        'search_value_1': project
    }
    headers = config['headers']
    req = requests.get(url, data= data,verify= False, headers= headers)
    return json.loads(req.text)

def get_vuln_by_submission_id (id):
    try:
        url = config["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id",id)
        data = {
            'oauth_token': config["formstack"]["token"],
        }
        headers = config['headers']
        req = requests.get(url, data= data ,verify= False, headers= headers)
        sub = parse_formstack_vuln_req(json.loads(req.text)["data"],id)
        sleep(1)
        return sub
    except:
        print ("ERROR de conexion")
        return []
        
def update_vuln_by_id(reinp):
    fieldCtx = config["formstack"]["fields"]["vuln"]
    #WRAP REQUEST POST PARAMS
    id = reinp['vuln[id]']
    files = {
        "field_" + fieldCtx["donde"] : reinp['vuln[donde]'],
        "field_" + fieldCtx["cardinalidad"] : reinp['vuln[cardinalidad]'],
        "field_" + fieldCtx["criticidad"] : reinp['vuln[criticidad]'],
        "field_" + fieldCtx["vulnerabilidad"] : reinp['vuln[vulnerabilidad]']
    }
    if "vuln[riesgo]" in reinp:
        files["field_"+fieldCtx["riesgo"]] = reinp['vuln[riesgo]']
    if "vuln[amenaza]" in reinp:
        files["field_"+fieldCtx["amenaza"]] = reinp['vuln[amenaza]']
    
    #DEFINE URL
    url = config["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id",id)
    url+= "?oauth_token=" +config["formstack"]["token"]
    headers = config['headers']
    headers["cache-control"] = "no-chache"
    headers["content-type"] = "application/x-www-form-urlencoded"
    req = None
    try:
        req = requests.put(url, data= files, headers= headers, verify= False)
    except:
        req = None
    finally:
        return req

def delete_vuln_by_id(reinp):
    analista = "glopez@fluid.la"
    fieldCtx = config["formstack"]["fields"]["delete"]
    url = config["formstack"]["forms"]["create_delete_registry"]
    url+= "?oauth_token=" +config["formstack"]["token"]
    data = {
        "field_" + fieldCtx["analista"] : analista,
        "field_" + fieldCtx["id"]: reinp['vuln[id]'],
        "field_" + fieldCtx["hallazgo"]: reinp['vuln[hallazgo]'],
        "field_" + fieldCtx["proyecto"]: reinp['vuln[proyecto_fluid]'],
        "field_" + fieldCtx["justificacion"]: reinp['vuln[justificacion]']
    }
    headers = config["headers"]
    register = None
    while(register == None):
        try:
            register = requests.post(url,data= data, headers= headers)
        except:
            register = None
    

def one_login_auth(username, password):
    url = config['onelogin']['url']
    data = {
        'username': username,
        'password': password,
        'api_key': config['onelogin']['api_key'],
        'app_id': config['onelogin']['app_id']
    }
    headers = config['headers']
    req = requests.post(url, data= data, headers= headers)
    result = json.loads(req.text)
    return result