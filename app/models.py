# -*- coding: utf-8 -*-
"""Funciones para consumir la API de Onelogin y Formstack"""
import json
from time import sleep
#from __future__ import unicode_literals
import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.adapters.DEFAULT_RETRIES = 10

CONFIG = {
    'headers':{
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
                      '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
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
            'get_evnt_by_name':{
                'url': 'https://www.formstack.com/api/v2/form/1886931/submission.json',
                'fields': {
                    'name': '29042322'
                }
            },
            'get_submission_by_id':{
                'url' : 'https://www.formstack.com/api/v2/submission/:id.json'
            },
            'get_order':{
                'url': 'https://www.formstack.com/api/v2/form/1925068/submission.json',
                'fields': {
                    'name': '48092369'
                }
            },
            'create_delete_registry':{
                'url': 'https://www.formstack.com/api/v2/form/2388563/submission.json'
            }
        },
        'fields':{
            'order':{
                'proyecto_fluid': '48092369'
            },
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
                #2016-nov-2 Agregado para documentacion automatica
                #2016-nov-2 Calificacion CVS
                'categoria': "46956845",
                'escenario': "38692215",
                'ambito': "38254691",
                'vector_acceso': "38529247",
                'complejidad_acceso': "38529248",
                'autenticacion': "38529249",
                'impacto_confidencialidad': "38529250",
                'impacto_integridad': "38529251",
                'impacto_disponibilidad': "38529252",
                'explotabilidad': "38529253",
                'nivel_resolucion': "38529254",
                'nivel_confianza': "38529255",
                'evidencia': "32202896",
                #2016-dic-12 Agregado para documentacion automatica
                #2016-dic-12 Campos para generar IE Fluid
                'sistema_comprometido': "48092123",
                'vector_ataque': "48092088"
            },
            'evnt':{
                'analista': "29042426",
                'cliente': "29042288",
                'proyecto_fluid': "29042322",
                'proyecto_cliente': "39595967",
                'tipo': "29042327",
                'detalle': "29042402",
                'fecha': "29042174",
                'estado': "29062640",
                'afectacion': "29042542"
            }
        }
    },
    'onelogin': {
        'url': 'https://api.onelogin.com/api/v3/saml/assertion',
        'api_key': 'e5996692a9bf56a66f8d4542948c47ac7913c505',
        'app_id': '476874'
    }
}

def parse_vulnreq(frmvuln, frmid):
    """Convierte los indices numericos de formstack
       a su respectivo nombre"""
    vuln = dict()
    config_frm = CONFIG["formstack"]["fields"]
    config_ctx = config_frm["vuln"]
    config_prj = config_frm["project"]
    vuln["id"] = frmid
    for i in frmvuln:
        #DETALLES VULNERABILIDAD
        if i["field"] == config_ctx["hallazgo"]:
            vuln["hallazgo"] = i["value"]
        if i["field"] == config_ctx["codigo_cliente"]:
            vuln["codigo_cliente"] = i["value"]
        if i["field"] == config_ctx["probabilidad"]:
            vuln["probabilidad"] = i["value"]
        if i["field"] == config_ctx["severidad"]:
            vuln["severidad"] = i["value"]
        if i["field"] == config_ctx["nivel_riesgo"]:
            vuln["nivel_riesgo"] = i["value"]
        if i["field"] == config_ctx["cardinalidad"]:
            vuln["cardinalidad"] = i["value"]
        if i["field"] == config_ctx["donde"]:
            vuln["donde"] = i["value"]
        if i["field"] == config_ctx["criticidad"]:
            vuln["criticidad"] = i["value"]
        if i["field"] == config_ctx["vulnerabilidad"]:
            vuln["vulnerabilidad"] = i["value"]
        if i["field"] == config_ctx["amenaza"]:
            vuln["amenaza"] = i["value"]
        if i["field"] == config_ctx["componente_aplicativo"]:
            vuln["componente_aplicativo"] = i["value"]
        if i["field"] == config_ctx["tipo_prueba"]:
            vuln["tipo_prueba"] = i["value"]
        if i["field"] == config_ctx["riesgo"]:
            vuln["riesgo"] = i["value"]
        if i["field"] == config_ctx["requisitos"]:
            vuln["requisitos"] = i["value"]
        if i["field"] == config_ctx["solucion_efecto"]:
            vuln["solucion_efecto"] = i["value"]
        if i["field"] == config_ctx["tipo"]:
            vuln["tipo"] = i["value"]
        if i["field"] == config_ctx["sistema_comprometido"]:
            vuln["sistema_comprometido"] = i["value"]
        if i["field"] == config_ctx["vector_ataque"]:
            vuln["vector_ataque"] = i["value"]
        #DETALLES PROYECTO
        if i["field"] == config_prj["analista"]:
            vuln["analista"] = i["value"]
        if i["field"] == config_prj["lider"]:
            vuln["lider"] = i["value"]
        if i["field"] == config_prj["interesado"]:
            vuln["interesado"] = i["value"]
        if i["field"] == config_prj["proyecto_fluid"]:
            vuln["proyecto_fluid"] = i["value"]
        if i["field"] == config_prj["proyecto_cliente"]:
            vuln["proyecto_cliente"] = i["value"]
        if i["field"] == config_prj["contexto"]:
            vuln["contexto"] = i["value"]
        if i["field"] == config_prj["nivel"]:
            vuln["nivel"] = i["value"]
        #2016-nov-2 Agregado para documentacion automatica
        #2016-nov-2 Calificacion CVS
        if i["field"] == config_ctx["vector_acceso"]:
            vuln["vector_acceso"] = i["value"]
        if i["field"] == config_ctx["complejidad_acceso"]:
            vuln["complejidad_acceso"] = i["value"]
        if i["field"] == config_ctx["autenticacion"]:
            vuln["autenticacion"] = i["value"]
        if i["field"] == config_ctx["impacto_confidencialidad"]:
            vuln["impacto_confidencialidad"] = i["value"]
        if i["field"] == config_ctx["impacto_integridad"]:
            vuln["impacto_integridad"] = i["value"]
        if i["field"] == config_ctx["impacto_disponibilidad"]:
            vuln["impacto_disponibilidad"] = i["value"]
        if i["field"] == config_ctx["explotabilidad"]:
            vuln["explotabilidad"] = i["value"]
        if i["field"] == config_ctx["nivel_resolucion"]:
            vuln["nivel_resolucion"] = i["value"]
        if i["field"] == config_ctx["nivel_confianza"]:
            vuln["nivel_confianza"] = i["value"]
        if i["field"] == config_ctx["evidencia"]:
            vuln["evidencia"] = i["value"]
        if i["field"] == config_ctx["escenario"]:
            vuln["escenario"] = i["value"]
        if i["field"] == config_ctx["ambito"]:
            vuln["ambito"] = i["value"]
        if i["field"] == config_ctx["categoria"]:
            vuln["categoria"] = i["value"]
    return vuln

def parse_evntreq(frmevnt, frmid):
    """Convierte los indices numericos de formstack
       a su respectivo nombre
    """
    evnt = dict()
    config_frm = CONFIG["formstack"]["fields"]
    config_ctx = config_frm["evnt"]
    evnt["id"] = frmid
    for i in frmevnt:
        #DETALLES VULNERABILIDAD
        if i["field"] == config_ctx["analista"]:
            evnt["analista"] = i["value"]
        if i["field"] == config_ctx["cliente"]:
            evnt["cliente"] = i["value"]
        if i["field"] == config_ctx["proyecto_fluid"]:
            evnt["proyecto_fluid"] = i["value"]
        if i["field"] == config_ctx["tipo"]:
            evnt["tipo"] = i["value"]
        if i["field"] == config_ctx["detalle"]:
            evnt["detalle"] = i["value"]
        if i["field"] == config_ctx["proyecto_cliente"]:
            evnt["proyecto_cliente"] = i["value"]
        if i["field"] == config_ctx["fecha"]:
            evnt["fecha"] = i["value"]
        if i["field"] == config_ctx["estado"]:
            evnt["estado"] = i["value"]
        if i["field"] == config_ctx["afectacion"]:
            evnt["afectacion"] = i["value"]
    return evnt

def get_vuln_by_name(project):
    """Obtiene todas las submission de un proyecto
       desde la API de Formstack"""
    url = CONFIG["formstack"]["forms"]["get_vuln_by_name"]["url"]
    data = {
        'oauth_token': CONFIG["formstack"]["token"],
        'search_field_1': CONFIG["formstack"]["forms"]["get_vuln_by_name"]["fields"]["name"],
        'search_value_1': project
    }
    result = False
    try:
        result = requests.get(url, data=data, verify=False, headers=CONFIG['headers'])
        result = json.loads(result.text)
    except requests.exceptions.SSLError:
        result = False #Formstack SSLError
    except requests.exceptions.Timeout:
        result = False #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = False #Fail token
    return result

def get_evnt_by_name(project):
    """Obtiene todas las eventualidades de un proyecto
       desde la API de Formstack"""
    url = CONFIG["formstack"]["forms"]["get_evnt_by_name"]["url"]
    data = {
        'oauth_token': CONFIG["formstack"]["token"],
        'search_field_1': CONFIG["formstack"]["forms"]["get_evnt_by_name"]["fields"]["name"],
        'search_value_1': project
    }
    result = None
    try:
        result = requests.get(url, data=data, verify=False, headers=CONFIG['headers'])
        result = json.loads(result.text)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result

def get_vuln_by_submission_id(vuln_id):
    """Obtiene los detalles del id de una submission
       desde la API de formstack"""
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id", vuln_id)
        data = {
            'oauth_token': CONFIG["formstack"]["token"],
        }
        form_req = requests.get(url, data=data, verify=False, headers=CONFIG['headers'])
        result = parse_vulnreq(json.loads(form_req.text)["data"], vuln_id)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    except KeyError:
        result = None #Not found id
    return result

def get_evnt_by_submission_id(evnt_id):
    """Obtiene los detalles del id de una submission
       desde la API de formstack"""
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id", evnt_id)
        data = {
            'oauth_token': CONFIG["formstack"]["token"],
        }
        form_req = requests.get(url, data=data, verify=False, headers=CONFIG['headers'])
        result = parse_evntreq(json.loads(form_req.text)["data"], evnt_id)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    except KeyError:
        result = None #Not found id
    return result

def update_vuln_by_id(data):
    """Actualiza una submission de formstack usando su id"""
    field_config = CONFIG["formstack"]["fields"]["vuln"]
    vuln_id = data['vuln[id]']
    files = {
        "field_" + field_config["donde"] : data['vuln[donde]'],
        "field_" + field_config["cardinalidad"] : data['vuln[cardinalidad]'],
        "field_" + field_config["criticidad"] : data['vuln[criticidad]'],
        "field_" + field_config["vulnerabilidad"] : data['vuln[vulnerabilidad]'],
        "field_" + field_config["amenaza"] : data['vuln[amenaza]'],
    }
    if data["vuln[nivel]"] == "General":
        files["field_"+field_config["vector_ataque"]] = data['vuln[vector_ataque]']
        files["field_"+field_config["sistema_comprometido"]] = data['vuln[sistema_comprometido]']
    else:
        files["field_"+field_config["riesgo"]] = data['vuln[riesgo]']
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id", vuln_id)
        url += "?oauth_token=" + CONFIG["formstack"]["token"]
        headers = CONFIG['headers']
        headers["cache-control"] = "no-cache"
        headers["content-type"] = "application/x-www-form-urlencoded"
        result = requests.put(url, data=files, headers=headers, verify=False)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result

def update_evnt_by_id(reinp):
    """Actualiza una eventualidad de formstack usando su id"""
    field_config = CONFIG["formstack"]["fields"]["evnt"]
    vuln_id = reinp['vuln[id]']
    files = {
        "field_" + field_config["afectacion"] : reinp['vuln[afectacion]'],
        "field_" + field_config["estado"] : "Tratada"
    }
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id", vuln_id)
        url += "?oauth_token=" + CONFIG["formstack"]["token"]
        headers = CONFIG['headers']
        headers["cache-control"] = "no-cache"
        headers["content-type"] = "application/x-www-form-urlencoded"
        result = requests.put(url, data=files, headers=headers, verify=False)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result

def delete_vuln_by_id(frmid):
    """Elimina un hallazgo usando su ID y genera un log en formstack
       con el nombre del analista
       TODO: Cambiar la url para eliminar, agregar logger desde el servicio
    """
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"]
        url = url.replace(":id", frmid) \
            + "?oauth_token=" \
            + CONFIG["formstack"]["token"]
        data = {
            "id" : frmid
        }
        headers = CONFIG['headers']
        headers["cache-control"] = "no-chache"
        headers["content-type"] = "application/x-www-form-urlencoded"
        result = requests.delete(url, data=data, headers=headers)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result

def one_login_auth(username, password):
    """Consume la API de OneLogin para autenticar un usuario"""
    url = CONFIG['onelogin']['url']
    data = {
        'username': username,
        'password': password,
        'api_key': CONFIG['onelogin']['api_key'],
        'app_id': CONFIG['onelogin']['app_id']
    }
    result = None
    try:
        req = requests.post(url, data=data, verify=False, headers=CONFIG['headers'])
        if req.status_code == 401:
            result = None
        elif req.status_code == 200:
            result = True
    except requests.exceptions.Timeout:
        result = None #One login Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail login
    return result

def get_order(project):
    """Obtiene el ID de pedido relacionado a un proyecto
       desde la API de Formstack"""
    url = CONFIG["formstack"]["forms"]["get_order"]["url"]
    data = {
        'oauth_token': CONFIG["formstack"]["token"],
        'search_field_1': CONFIG["formstack"]["forms"]["get_order"]["fields"]["name"],
        'search_value_1': project
    }
    result = None
    try:
        result = requests.get(url, data=data, verify=False, headers=CONFIG['headers'])
        result = json.loads(result.text)
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result

def update_order_id(project, order_id):
    """ Actualiza el nombre de proyecto en un pedido de formstack """
    field_config = CONFIG["formstack"]["fields"]["order"]
    files = {
        "field_" + field_config["proyecto_fluid"] : project
    }
    result = None
    try:
        url = CONFIG["formstack"]["forms"]["get_submission_by_id"]["url"].replace(":id", order_id)
        url += "?oauth_token=" + CONFIG["formstack"]["token"]
        headers = CONFIG['headers']
        headers["cache-control"] = "no-cache"
        headers["content-type"] = "application/x-www-form-urlencoded"
        result = requests.put(url, data=files, headers=headers, verify=False)
        print result.status_code
        print result
    except requests.exceptions.SSLError:
        result = None #Formstack SSLError
    except requests.exceptions.Timeout:
        result = None #Formstack Connection timeout
    except requests.exceptions.HTTPError:
        result = None #Fail token
    return result