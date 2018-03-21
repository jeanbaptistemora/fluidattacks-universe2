"""DTO para mapear los campos de integrates a formstack"""
# pylint: disable=E0402
class FindingDTO(object):
    """ Clase para crear un objeto con los atributos de un hallazgo """

    #Atributos proyecto
    ANALISTA = "32201744"
    LIDER = "38193323"
    INTERESADO = "38392409"
    PROYECTO_FLUID = "32201732"
    PROYECTO_CLIENTE = "38209122"
    CONTEXTO = "38404474"

    #Atributos evidencia
    REVISION = "54856382"
    DOC_TOTAL = "53714016"
    DOC_ACHV1 = "32202896"
    DOC_ACHV2 = "53713035"
    DOC_ACHV3 = "53713045"
    DOC_ACHV4 = "53714414"
    DOC_ACHV5 = "53714452"
    DOC_CMNT1 = "53713106"
    DOC_CMNT2 = "53713149"
    DOC_CMNT3 = "53713153"
    DOC_CMNT4 = "53714417"
    DOC_CMNT5 = "53714455"
    ANIMATION = "38307272"
    EXPLOTATION = "38307222"
    EXPLOIT = "38307199"
    REG = "53609444"
    REG_NUM = "49412242"
    REG_FILE = "49412246"

    #Atributos descriptivos
    CLASE = "38392454" #detallado
    HALLAZGO = "32201810"
    SUSCRIPCION = "54346108"
    CODIGO_CLIENTE = "38193365"
    PROBABILIDAD = "38193660"
    SEVERIDAD = "38193659"
    NIVEL_RIESGO = "38194645"
    VALOR_RIESGO = "38194645"
    CARDINALIDAD = "38255025"
    DONDE = "38193357"
    CRITICIDAD = "38531129"
    VULNERABILIDAD = "32202728"
    AMENAZA = "38193361"
    COMPONENTE_APLICATIVO = "38209122"
    TIPO_PRUEBA = "38254692"
    TIPO_HALLAZGO = "54319180"
    RIESGO = "38193362"
    REQUISITOS = "38254586"
    SOLUCION_EFECTO = "38619077"
    KB = "38861739"
    TIPO = "38392454"
    ACTOR = "38606398"
    CATEGORIA = "46956845"
    ESCENARIO = "38692215"
    AMBITO = "38254691"
    SISTEMA_COMPROMETIDO = "48092123"
    VECTOR_ATAQUE = "48092088"
    CWE = "38899046"
    TRATAMIENTO = "59350064"
    RAZON_TRATAMIENTO = "59351642"
    RESPONSABLE_TRATAMIENTO = "59381058"
    BTS_EXTERNO = "56614832"

    #Atributos CssV2
    VECTOR_ACCESO = "38529247"
    COMPLEJIDAD_ACCESO = "38529248"
    AUTENTICACION = "38529249"
    EXPLOTABILIDAD = "38529253"
    CRITICIDAD = "38531129"
    IMPACTO_CONFIDENCIALIDAD = "38529250"
    IMPACTO_INTEGRIDAD = "38529251"
    IMPACTO_DISPONIBILIDAD = "38529252"
    NIVEL_RESOLUCION = "38529254"
    NIVEL_CONFIANZA = "38529255"

    def __init__(self):
        """ Constructor de la clase """
        self.request_id = None
        self.data = dict()

    def create(self, parameter):
        self.create_description(parameter)
        self.create_cssv2(parameter)

    def create_evidence_description(self, parameter): # noqa: C901
        """ Convierte los indices de un JSON a indices
            de Formstack """
        if "data[id]" in parameter:
            self.request_id \
                = parameter["data[id]"]
        if "data[" + parameter["data[field]"] + "]" in parameter:
            if parameter["data[field]"] == "desc_evidencia_1":
                self.data[self.DOC_CMNT1] \
                = parameter["data[" + parameter["data[field]"] + "]"]
            if parameter["data[field]"] == "desc_evidencia_2":
                self.data[self.DOC_CMNT2] \
                = parameter["data[" + parameter["data[field]"] + "]"]
            if parameter["data[field]"] == "desc_evidencia_3":
                self.data[self.DOC_CMNT3] \
                = parameter["data[" + parameter["data[field]"] + "]"]
            if parameter["data[field]"] == "desc_evidencia_4":
                self.data[self.DOC_CMNT4] \
                = parameter["data[" + parameter["data[field]"] + "]"]
            if parameter["data[field]"] == "desc_evidencia_5":
                self.data[self.DOC_CMNT5] \
                = parameter["data[" + parameter["data[field]"] + "]"]
    def create_description(self, parameter): # noqa: C901
        """ Convierte los indices de un JSON a indices
            de Formstack """
        if "data[id]" in parameter:
            self.request_id \
                = parameter["data[id]"]
        if "data[hallazgo]" in parameter:
            self.data[self.HALLAZGO] \
                = parameter["data[hallazgo]"]
        if "data[escenario]" in parameter:
            self.data[self.ESCENARIO] \
                = parameter["data[escenario]"]
        if "data[cardinalidad]" in parameter:
            self.data[self.CARDINALIDAD] \
                = parameter["data[cardinalidad]"]
        if "data[actor]" in parameter:
            self.data[self.ACTOR] \
                = parameter["data[actor]"]
        if "data[vulnerabilidad]" in parameter:
            self.data[self.VULNERABILIDAD] \
                = parameter["data[vulnerabilidad]"]
        if "data[requisitos]" in parameter:
            self.data[self.REQUISITOS] \
                = parameter["data[requisitos]"]
        if "data[donde]" in parameter:
            self.data[self.DONDE] \
                = parameter["data[donde]"]
        if "data[solucion_efecto]" in parameter:
            self.data[self.SOLUCION_EFECTO] \
                = parameter["data[solucion_efecto]"]
        if "data[amenaza]" in parameter:
            self.data[self.AMENAZA] \
                = parameter["data[amenaza]"]
        if "data[vector_ataque]" in parameter:
            self.data[self.VECTOR_ATAQUE] \
                = parameter["data[vector_ataque]"]
        if "data[sistema_comprometido]" in parameter:
            self.data[self.SISTEMA_COMPROMETIDO] \
                = parameter["data[sistema_comprometido]"]
        if "data[cwe]" in parameter:
            self.data[self.CWE] \
                = parameter["data[cwe]"]
        if "data[registros]" in parameter:
            self.data[self.REG] \
                = parameter["data[registros]"]
        if "data[registros_num]" in parameter:
            self.data[self.REG_NUM] \
                = parameter["data[registros_num]"]
        if "data[nivel]" in parameter:
            self.data[self.CLASE] \
                = parameter["data[nivel]"]
            if self.data[self.CLASE] == "Detallado":
                if "data[categoria]" in parameter:
                    self.data[self.CATEGORIA] \
                        = parameter["data[categoria]"]
                if "data[valor_riesgo]" in parameter:
                    self.data[self.VALOR_RIESGO] \
                        = parameter["data[valor_riesgo]"]
                if "data[probabilidad]" in parameter:
                    self.data[self.PROBABILIDAD] \
                        = parameter["data[probabilidad]"]
                if "data[severidad]" in parameter:
                    self.data[self.SEVERIDAD] \
                        = parameter["data[severidad]"]

    def create_treatment(self, parameter):
        """ Convierte los indices de un JSON a indices
            de Formstack """
        if "data[id]" in parameter:
            self.request_id \
                = parameter["data[id]"]
        if "data[tratamiento]" in parameter:
            self.data[self.TRATAMIENTO] \
                = parameter["data[tratamiento]"]
        if "data[razon_tratamiento]" in parameter:
            self.data[self.RAZON_TRATAMIENTO] \
                = parameter["data[razon_tratamiento]"]
        if "data[responsable_tratamiento]" in parameter:
            self.data[self.RESPONSABLE_TRATAMIENTO] \
                = parameter["data[responsable_tratamiento]"]
        if "data[bts_externo]" in parameter:
            self.data[self.BTS_EXTERNO] \
                = parameter["data[bts_externo]"]

    def create_cssv2(self, parameter):
        """ Convierte los indices de un JSON a indices
            de Formstack """
        if "data[id]" in parameter:
            self.request_id \
                = parameter["data[id]"]
        if "data[vector_acceso]" in parameter:
            self.data[self.VECTOR_ACCESO] \
                = parameter["data[vector_acceso]"]
        if "data[complejidad_acceso]" in parameter:
            self.data[self.COMPLEJIDAD_ACCESO] \
                = parameter["data[complejidad_acceso]"]
        if "data[autenticacion]" in parameter:
            self.data[self.AUTENTICACION] \
                = parameter["data[autenticacion]"]
        if "data[explotabilidad]" in parameter:
            self.data[self.EXPLOTABILIDAD] \
                = parameter["data[explotabilidad]"]
        if "data[criticidad]" in parameter:
            self.data[self.CRITICIDAD] \
                = parameter["data[criticidad]"]
        if "data[impacto_confidencialidad]" in parameter:
            self.data[self.IMPACTO_CONFIDENCIALIDAD] \
                = parameter["data[impacto_confidencialidad]"]
        if "data[impacto_integridad]" in parameter:
            self.data[self.IMPACTO_INTEGRIDAD] \
                = parameter["data[impacto_integridad]"]
        if "data[impacto_disponibilidad]" in parameter:
            self.data[self.IMPACTO_DISPONIBILIDAD] \
                = parameter["data[impacto_disponibilidad]"]
        if "data[nivel_resolucion]" in parameter:
            self.data[self.NIVEL_RESOLUCION] \
                = parameter["data[nivel_resolucion]"]
        if "data[nivel_confianza]" in parameter:
            self.data[self.NIVEL_CONFIANZA] \
                = parameter["data[nivel_confianza]"]

    def create_delete(self, parameter, analyst, project, finding):
        """ Crea un set de datos para enviar en el correo
            de eliminacion de hallazgo """
        return {
            'mail_analista': analyst,
            'name_finding': finding,
            'id_finding': parameter["data[id]"],
            'description': parameter["data[justificacion]"],
            'project': project,
        }

    def parse(self, submission_id, request_arr, sess_obj):
        self.data = dict()
        self.data["id"] = submission_id
        self.data["timestamp"] = request_arr["timestamp"]
        if sess_obj is not None:
            sess_obj.session["drive_urls"] = []
        self.parse_description(request_arr)
        self.parse_cssv2(request_arr)
        self.parse_project(request_arr)
        self.parse_evidence_info(request_arr, sess_obj)
        return self.data

    def parse_vulns_by_id(self, submission_id, request_arr):
        self.data = dict()
        self.data["id"] = submission_id
        self.data["timestamp"] = request_arr["timestamp"]
        self.parse_description(request_arr)
        return self.data

    def parse_description(self, request_arr): # noqa: C901
        "Convierte la descripcion de un hallazgo en formstack"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.HALLAZGO:
                self.data["hallazgo"] = finding["value"]
            if finding["field"] == self.SUSCRIPCION:
                self.data["suscripcion"] = finding["value"]
            if finding["field"] == self.CODIGO_CLIENTE:
                self.data["codigo_cliente"] = finding["value"]
            if finding["field"] == self.PROBABILIDAD:
                self.data["probabilidad"] = finding["value"]
            if finding["field"] == self.SEVERIDAD:
                self.data["severidad"] = finding["value"]
            if finding["field"] == self.NIVEL_RIESGO:
                self.data["nivel_riesgo"] = finding["value"]
            if finding["field"] == self.CARDINALIDAD:
                self.data["cardinalidad"] = finding["value"]
            if finding["field"] == self.DONDE:
                self.data["donde"] = finding["value"]
            if finding["field"] == self.CRITICIDAD:
                self.data["criticidad"] = finding["value"]
                criticity = float(finding["value"])
                if(criticity <= 3.9):
                    self.data["impacto"] = "Bajo"
                elif(criticity <= 6.9):
                    self.data["impacto"] = "Medio"
                else:
                    self.data["impacto"] = "Alto"
            if finding["field"] == self.VULNERABILIDAD:
                self.data["vulnerabilidad"] = finding["value"]
            if finding["field"] == self.AMENAZA:
                self.data["amenaza"] = finding["value"]
            if finding["field"] == self.COMPONENTE_APLICATIVO:
                self.data["componente_aplicativo"] = finding["value"]
            if finding["field"] == self.TIPO_PRUEBA:
                self.data["tipo_prueba"] = finding["value"]
            if finding["field"] == self.RIESGO:
                self.data["riesgo"] = finding["value"]
            if finding["field"] == self.REQUISITOS:
                self.data["requisitos"] = finding["value"]
            if finding["field"] == self.SOLUCION_EFECTO:
                self.data["solucion_efecto"] = finding["value"]
            if finding["field"] == self.KB:
                self.data["kb"] = finding["value"]
            if finding["field"] == self.TIPO:
                self.data["tipo"] = finding["value"]
            if finding["field"] == self.SISTEMA_COMPROMETIDO:
                self.data["sistema_comprometido"] = finding["value"]
            if finding["field"] == self.VECTOR_ATAQUE:
                self.data["vector_ataque"] = finding["value"]
            if finding["field"] == self.TIPO_HALLAZGO:
                self.data["tipo_hallazgo"] = finding["value"]
            if finding["field"] == self.REVISION:
                self.data["revision"] = finding["value"]
            if finding["field"] == self.ESCENARIO:
                self.data["escenario"] = finding["value"]
            if finding["field"] == self.AMBITO:
                self.data["ambito"] = finding["value"]
            if finding["field"] == self.CATEGORIA:
                self.data["categoria"] = finding["value"]
            if finding["field"] == self.ACTOR:
                self.data["actor"] = finding["value"]
            if finding["field"] == self.TRATAMIENTO:
                self.data["tratamiento"] = finding["value"]
            if finding["field"] == self.RAZON_TRATAMIENTO:
                self.data["razon_tratamiento"] = finding["value"]
            if finding["field"] == self.RESPONSABLE_TRATAMIENTO:
                self.data["responsable_tratamiento"] = finding["value"]
            if finding["field"] == self.BTS_EXTERNO:
                self.data["bts_externo"] = finding["value"]
            if finding["field"] == self.CWE:
                try:
                    value = int(finding["value"])
                    urlbase = 'https://cwe.mitre.org/data/definitions/:id.html'
                    self.data["cwe"] = urlbase.replace(':id', str(value))
                except ValueError:
                    self.data["cwe"] = 'None'

    def parse_description_mail(self, request_arr): # noqa: C901
        "Convierte la descripcion de un hallazgo en formstack para envio de mail"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.HALLAZGO:
                self.data["hallazgo"] = finding["value"]
        return self.data

    def parse_description_vuln(self, request_arr): # noqa: C901
        "Convierte la descripcion de un hallazgo en formstack"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.CARDINALIDAD:
                self.data["cardinalidad"] = finding["value"]
        return self.data

    def parse_cssv2(self, request_arr): # noqa: C901
        "Convierte la califiacion de un hallazgo en formstack"
        for finding in request_arr["data"]:
            if finding["field"] == self.VECTOR_ACCESO:
                self.data["vector_acceso"] = finding["value"]
            if finding["field"] == self.COMPLEJIDAD_ACCESO:
                self.data["complejidad_acceso"] = finding["value"]
            if finding["field"] == self.AUTENTICACION:
                self.data["autenticacion"] = finding["value"]
            if finding["field"] == self.IMPACTO_CONFIDENCIALIDAD:
                self.data["impacto_confidencialidad"] = finding["value"]
            if finding["field"] == self.IMPACTO_INTEGRIDAD:
                self.data["impacto_integridad"] = finding["value"]
            if finding["field"] == self.IMPACTO_DISPONIBILIDAD:
                self.data["impacto_disponibilidad"] = finding["value"]
            if finding["field"] == self.EXPLOTABILIDAD:
                self.data["explotabilidad"] = finding["value"]
            if finding["field"] == self.NIVEL_RESOLUCION:
                self.data["nivel_resolucion"] = finding["value"]
            if finding["field"] == self.NIVEL_CONFIANZA:
                self.data["nivel_confianza"] = finding["value"]
        if self.data['explotabilidad'] == '1.000 | Alta: No se requiere exploit o se puede automatizar' \
            or self.data['explotabilidad'] == '0.950 | Funcional: Existe exploit':
            self.data['explotable'] = 'Si'
        else:
            self.data['explotable'] = 'No'
        if 'tipo_hallazgo' not in self.data or self.data['tipo_hallazgo'] == 'Seguridad':
            self.data['tipo_hallazgo_cliente'] = 'Vulnerabilidad'
        else:
            self.data['tipo_hallazgo_cliente'] = self.data['tipo_hallazgo']

    def parse_project(self, request_arr):
        "Convierte la info de proyecto de un hallazgo en formstack"
        for finding in request_arr["data"]:
            if finding["field"] == self.ANALISTA:
                self.data["analista"] = finding["value"]
            if finding["field"] == self.LIDER:
                self.data["lider"] = finding["value"]
            if finding["field"] == self.INTERESADO:
                self.data["interesado"] = finding["value"]
            if finding["field"] == self.PROYECTO_FLUID:
                self.data["proyecto_fluid"] = finding["value"]
            if finding["field"] == self.PROYECTO_CLIENTE:
                self.data["proyecto_cliente"] = finding["value"]
            if finding["field"] == self.CONTEXTO:
                self.data["contexto"] = finding["value"]

    def parse_evidence_info(self, request_arr, sess_obj): # noqa: C901
        "Convierte la descripcion de un request de formstack"
        for finding in request_arr["data"]:
            if finding["field"] == self.DOC_TOTAL:
                self.data["total_evidencias"] = finding["value"]
            if finding["field"] == self.DOC_ACHV1:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["ruta_evidencia_1"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.DOC_ACHV2:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["ruta_evidencia_2"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.DOC_ACHV3:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["ruta_evidencia_3"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.DOC_ACHV4:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["ruta_evidencia_4"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.DOC_ACHV5:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["ruta_evidencia_5"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.ANIMATION:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["animacion"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.EXPLOTATION:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["explotacion"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.EXPLOIT:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["exploit"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.REG_FILE:
                filtered_url = self.drive_url_filter(finding["value"])
                self.data["registros_archivo"] = filtered_url
                if sess_obj is not None:
                    sess_obj.session[filtered_url] = 1
            if finding["field"] == self.DOC_CMNT1:
                self.data["desc_evidencia_1"] = finding["value"]
            if finding["field"] == self.DOC_CMNT2:
                self.data["desc_evidencia_2"] = finding["value"]
            if finding["field"] == self.DOC_CMNT3:
                self.data["desc_evidencia_3"] = finding["value"]
            if finding["field"] == self.DOC_CMNT4:
                self.data["desc_evidencia_4"] = finding["value"]
            if finding["field"] == self.DOC_CMNT5:
                self.data["desc_evidencia_5"] = finding["value"]
            if finding["field"] == self.REG:
                self.data["registros"] = finding["value"]
            if finding["field"] == self.REG_NUM:
                self.data["registros_num"] = finding["value"]

    def drive_url_filter(self, drive):
        """ Obtiene el ID de la imagen de drive """
        if(drive.find("s3.amazonaws.com") != -1):
            new_url = drive.split("/")[5]
            return new_url
        else:
            if(drive.find("id=") != -1):
                new_url = drive.split("id=")[1]
                if(new_url.find("&") != -1):
                    return new_url.split("&")[0]
        return drive

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data
