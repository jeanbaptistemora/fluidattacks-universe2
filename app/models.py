# -*- coding: utf-8 -*-
"""Funciones para consumir la API de Onelogin y Formstack"""

import json
from time import sleep
#from __future__ import unicode_literals
import requests
from requests.exceptions import ConnectionError
from retrying import retry
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.adapters.DEFAULT_RETRIES = 10
from .exceptions import APIConnectionException

class FormstackRequestMapper(object):
    """ Clase para cambiar los indices a nombres en un request """
    PROJECT_ANALISTA = "32201744"
    PROJECT_LIDER = "38193323"
    PROJECT_INTERESADO = "38392409"
    PROJECT_PROYECTO_FLUID = "32201732"
    PROJECT_PROYECTO_CLIENTE = "38209122"
    PROJECT_TIPO_PRUEBA = "38254692"
    PROJECT_CONTEXTO = "38404474"
    PROJECT_NIVEL = "38392454"

    EVENTUALITY_ANALISTA = "29042426"
    EVENTUALITY_CLIENTE = "29042288"
    EVENTUALITY_PROYECTO_FLUID = "29042322"
    EVENTUALITY_PROYECTO_CLIENTE = "39595967"
    EVENTUALITY_TIPO = "29042327"
    EVENTUALITY_DETALLE = "29042402"
    EVENTUALITY_FECHA = "29042174"
    EVENTUALITY_ESTADO = "29062640"
    EVENTUALITY_AFECTACION = "29042542"

    FINDING_HALLAZGO = "32201810"
    FINDING_CODIGO_CLIENTE = "38193365"
    FINDING_PROBABILIDAD = "38193660"
    FINDING_SEVERIDAD = "38193659"
    FINDING_NIVEL_RIESGO = "38194645"
    FINDING_CARDINALIDAD = "38255025"
    FINDING_DONDE = "38193357"
    FINDING_CRITICIDAD = "38531129"
    FINDING_VULNERABILIDAD = "32202728"
    FINDING_AMENAZA = "38193361"
    FINDING_COMPONENTE_APLICATIVO = "38209122"
    FINDING_TIPO_PRUEBA = "38254692"
    FINDING_RIESGO = "38193362"
    FINDING_REQUISITOS = "38254586"
    FINDING_SOLUCION_EFECTO = "38619077"
    FINDING_TIPO = "38392454"
    FINDING_CATEGORIA = "46956845"
    FINDING_ESCENARIO = "38692215"
    FINDING_AMBITO = "38254691"
    FINDING_VECTOR_ACCESO = "38529247"
    FINDING_COMPLEJIDAD_ACCESO = "38529248"
    FINDING_AUTENTICACION = "38529249"
    FINDING_IMPACTO_CONFIDENCIALIDAD = "38529250"
    FINDING_IMPACTO_INTEGRIDAD = "38529251"
    FINDING_IMPACTO_DISPONIBILIDAD = "38529252"
    FINDING_EXPLOTABILIDAD = "38529253"
    FINDING_NIVEL_RESOLUCION = "38529254"
    FINDING_NIVEL_CONFIANZA = "38529255"
    FINDING_EVIDENCIA = "32202896"
    FINDING_SISTEMA_COMPROMETIDO = "48092123"
    FINDING_VECTOR_ATAQUE = "48092088"

    def map_finding(self, finding_request):
        """ Convierte los campos de un JSON hallazgo
            de Formstack para manipularlos en integrates """
        parsed = dict()
        for finding in finding_request["data"]:
            #DETALLES VULNERABILIDAD
            if finding["field"] == self.FINDING_HALLAZGO:
                parsed["hallazgo"] = finding["value"]
            if finding["field"] == self.FINDING_CODIGO_CLIENTE:
                parsed["codigo_cliente"] = finding["value"]
            if finding["field"] == self.FINDING_PROBABILIDAD:
                parsed["probabilidad"] = finding["value"]
            if finding["field"] == self.FINDING_SEVERIDAD:
                parsed["severidad"] = finding["value"]
            if finding["field"] == self.FINDING_NIVEL_RIESGO:
                parsed["nivel_riesgo"] = finding["value"]
            if finding["field"] == self.FINDING_CARDINALIDAD:
                parsed["cardinalidad"] = finding["value"]
            if finding["field"] == self.FINDING_DONDE:
                parsed["donde"] = finding["value"]
            if finding["field"] == self.FINDING_CRITICIDAD:
                parsed["criticidad"] = finding["value"]
            if finding["field"] == self.FINDING_VULNERABILIDAD:
                parsed["vulnerabilidad"] = finding["value"]
            if finding["field"] == self.FINDING_AMENAZA:
                parsed["amenaza"] = finding["value"]
            if finding["field"] == self.FINDING_COMPONENTE_APLICATIVO:
                parsed["componente_aplicativo"] = finding["value"]
            if finding["field"] == self.FINDING_TIPO_PRUEBA:
                parsed["tipo_prueba"] = finding["value"]
            if finding["field"] == self.FINDING_RIESGO:
                parsed["riesgo"] = finding["value"]
            if finding["field"] == self.FINDING_REQUISITOS:
                parsed["requisitos"] = finding["value"]
            if finding["field"] == self.FINDING_SOLUCION_EFECTO:
                parsed["solucion_efecto"] = finding["value"]
            if finding["field"] == self.FINDING_TIPO:
                parsed["tipo"] = finding["value"]
            if finding["field"] == self.FINDING_SISTEMA_COMPROMETIDO:
                parsed["sistema_comprometido"] = finding["value"]
            if finding["field"] == self.FINDING_VECTOR_ATAQUE:
                parsed["vector_ataque"] = finding["value"]
            if finding["field"] == self.FINDING_VECTOR_ACCESO:
                parsed["vector_acceso"] = finding["value"]
            if finding["field"] == self.FINDING_COMPLEJIDAD_ACCESO:
                parsed["complejidad_acceso"] = finding["value"]
            if finding["field"] == self.FINDING_AUTENTICACION:
                parsed["autenticacion"] = finding["value"]
            if finding["field"] == self.FINDING_IMPACTO_CONFIDENCIALIDAD:
                parsed["impacto_confidencialidad"] = finding["value"]
            if finding["field"] == self.FINDING_IMPACTO_INTEGRIDAD:
                parsed["impacto_integridad"] = finding["value"]
            if finding["field"] == self.FINDING_IMPACTO_DISPONIBILIDAD:
                parsed["impacto_disponibilidad"] = finding["value"]
            if finding["field"] == self.FINDING_EXPLOTABILIDAD:
                parsed["explotabilidad"] = finding["value"]
            if finding["field"] == self.FINDING_NIVEL_RESOLUCION:
                parsed["nivel_resolucion"] = finding["value"]
            if finding["field"] == self.FINDING_NIVEL_CONFIANZA:
                parsed["nivel_confianza"] = finding["value"]
            if finding["field"] == self.FINDING_EVIDENCIA:
                parsed["evidencia"] = finding["value"]
            if finding["field"] == self.FINDING_ESCENARIO:
                parsed["escenario"] = finding["value"]
            if finding["field"] == self.FINDING_AMBITO:
                parsed["ambito"] = finding["value"]
            if finding["field"] == self.FINDING_CATEGORIA:
                parsed["categoria"] = finding["value"]
            #DETALLES PROYECTO
            if finding["field"] == self.PROJECT_ANALISTA:
                parsed["analista"] = finding["value"]
            if finding["field"] == self.PROJECT_LIDER:
                parsed["lider"] = finding["value"]
            if finding["field"] == self.PROJECT_INTERESADO:
                parsed["interesado"] = finding["value"]
            if finding["field"] == self.PROJECT_PROYECTO_FLUID:
                parsed["proyecto_fluid"] = finding["value"]
            if finding["field"] == self.PROJECT_PROYECTO_CLIENTE:
                parsed["proyecto_cliente"] = finding["value"]
            if finding["field"] == self.PROJECT_CONTEXTO:
                parsed["contexto"] = finding["value"]
            if finding["field"] == self.PROJECT_NIVEL:
                parsed["nivel"] = finding["value"]
        parsed["id"] = finding_request["id"]
        return parsed

    def map_eventuality(self, eventuality_request):
        """ Convierte los campos de un JSON eventualidad
            de Formstack para manipularlos en integrates """
        parsed = dict()
        for eventuality in eventuality_request["data"]:
            if eventuality["field"] == self.EVENTUALITY_ANALISTA:
                parsed["analista"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_CLIENTE:
                parsed["cliente"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_PROYECTO_FLUID:
                parsed["proyecto_fluid"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_PROYECTO_CLIENTE:
                parsed["proyecto_cliente"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_TIPO:
                parsed["tipo"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_DETALLE:
                parsed["detalle"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_FECHA:
                parsed["fecha"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_ESTADO:
                parsed["estado"] = eventuality["value"]
            if eventuality["field"] == self.EVENTUALITY_AFECTACION:
                parsed["afectacion"] = eventuality["value"]
        parsed["id"] = eventuality_request["id"]
        return parsed

class FormstackAPI(object):

    headers_config = {}
    TOKEN = "aefb128ba610da7e8d9e0b6ff86d9d7a"

    def __init__(self):
        " Constructor "
        self.headers_config['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) FLUIDIntegrates/1.0'

    @retry(retry_on_exception=ConnectionError, stop_max_attempt_number=5)
    def request(self, method, url, data=None):
        " Construye las peticiones usadas para consultar Formstack "
        executed_request = None
        try:
            if method != "GET":
                self.headers_config["cache-control"] = "no-cache"
                self.headers_config["content-type"] = "application/x-www-form-urlencoded"
                url += "?oauth_token=:token".replace(":token", self.TOKEN)
            else:
                if not data:
                    data = {"oauth_token": self.TOKEN}
                else:
                    data["oauth_token"] = self.TOKEN
            formstack_request = requests.request(
                method, url,
                data=data, headers=self.headers_config
            )
            executed_request = json.loads(formstack_request.text)
        except ConnectionError:
            executed_request = None #Fail connection
        except requests.exceptions.SSLError:
            executed_request = None #Formstack SSLError
        except requests.exceptions.Timeout:
            executed_request = None #Formstack Connection timeout
        except requests.exceptions.HTTPError:
            executed_request = None #Fail token
        except ValueError: #Fail json format
            executed_request = None
        except TypeError: #Fail json
            executed_request = None
        return executed_request

    def delete_finding(self, submission_id):
        " Elimina una submission del formulario de hallazgos a partir de su id \
          TODO: como probar un test que elimina datos, un metodo que \
          recibe vars por post "
        url = "https://www.formstack.com" 
        url += "/api/v2/submission/:id.json"
        url = url.replace(":id", submission_id)
        data = {
            "id" : submission_id
        }
        return self.request("DELETE", url, data=data)

    def get_submission(self, submission_id):
        " Obtiene un submission a partir de su ID "
        url = "https://www.formstack.com/api/v2/submission/:id.json"
        url = url.replace(":id", submission_id)
        return self.request("GET", url)

    def get_findings(self, project):
        " Obtiene los hallazgos de un proyecto a partir del nombre de proyecto "
        url = "https://www.formstack.com/api/v2/form/1998500/submission.json"
        search_field = "32201732"
        data = {'search_field_1': search_field, 'search_value_1': project}
        return self.request("GET", url, data=data)

    def get_eventualities(self, project):
        " Obtiene las eventualidades de un proyecto a partir del nombre de proyecto "
        url = "https://www.formstack.com"
        url += "/api/v2/form/1886931/submission.json"
        search_field = "29042322"
        data = {'search_field_1': search_field, 'search_value_1': project}
        return self.request("GET", url, data=data)

    def get_order(self, project):
        " Obtiene un pedido bancolombia a partir del nombre de proyecto "
        #url = "https://www.formstack.com/api/v2/form/1925068/submission.json"
        url = "https://www.formstack.com/api/v2/form/1893765/submission.json"
        search_field = "48092369"
        data = {'search_field_1': search_field, 'search_value_1': project}
        return self.request("GET", url, data=data)

    def update_eventuality(self, afectacion, submission_id):
        " Actualiza una eventualidad en Formstack "
        url = "https://www.formstack.com/api/v2/submission/:id.json"
        url = url.replace(":id", submission_id)
        field_afectacion = "field_29042542"
        field_estado = "field_29062640"
        data = {
            field_afectacion: afectacion,
            field_estado: "Tratada"
        }
        return self.request("PUT", url, data=data)
    
    def update_finding(self, data_set, submission_id):
        " Actualiza un hallazgo en formstack "
        url = "https://www.formstack.com/api/v2/submission/:id.json"
        url = url.replace(":id", submission_id)
        field_donde = "field_38193357"
        field_cardinalidad = "field_38255025"
        field_criticidad = "field_38531129"
        field_vulnerabilidad = "field_32202728"
        field_amenaza = "field_38193361"
        field_vector_ataque = "field_48092088"
        field_sist_compro = "field_48092123"
        field_riesgo = "field_38193362"
        field_requisitos = "field_38254586"
        data = {
            field_donde: data_set['vuln[donde]'],
            field_cardinalidad: data_set['vuln[cardinalidad]'],
            field_criticidad: data_set['vuln[criticidad]'],
            field_vulnerabilidad: data_set['vuln[vulnerabilidad]'],
            field_amenaza: data_set['vuln[amenaza]'],
            field_requisitos: data_set['vuln[requisitos]']
        }
        if data_set["vuln[nivel]"] == "General":
            data[field_vector_ataque] = data_set['vuln[vector_ataque]']
            data[field_sist_compro] = data_set['vuln[sistema_comprometido]']
        else:
            data[field_riesgo] = data_set['vuln[riesgo]']
        return self.request("PUT", url, data=data)

    def update_order(self, project, submission_id):
        " Actualiza la relacion pedido bancolombia y proyecto en Formstack "
        url = "https://www.formstack.com/api/v2/submission/:id.json"
        url = url.replace(":id", submission_id)
        field_proyecto_fluid = "field_48092369"
        data = {field_proyecto_fluid: project}
        return self.request("PUT", url, data=data)

class OneLoginAPI(object):
    """ Wrap de la API de OneLogin """
    
    API_KEY = "e5996692a9bf56a66f8d4542948c47ac7913c505"
    APP_ID = "476874"
    headers_config = {} 
    username = ""
    password = ""

    def __init__(self, username, password):
        """ Constructor """
        self.username = username
        self.password = password
        self.headers_config['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) FLUIDIntegrates/1.0'

    def login(self):
        " Autentica un usuario utilizando la API de OneLogin "
        url = "https://api.onelogin.com/api/v3/saml/assertion"
        data = {
            'username': self.username,
            'password': self.password,
            'api_key': self.API_KEY,
            'app_id': self.APP_ID
        }
        result = False
        try:
            req = requests.post(url, data=data, verify=False, headers=self.headers_config)
            if req.status_code == 200:
                result = True
        except requests.exceptions.Timeout:
            result = False #One login Connection timeout
        except requests.exceptions.HTTPError:
            result = False #Fail login
        return result
