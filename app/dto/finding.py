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

    #Atributos descriptivos
    CLASE = "38392454" #detallado
    HALLAZGO = "32201810"
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
    TIPO = "38392454"
    ACTOR = "38606398"
    CATEGORIA = "46956845"
    ESCENARIO = "38692215"
    AMBITO = "38254691"
    SISTEMA_COMPROMETIDO = "48092123"
    VECTOR_ATAQUE = "48092088"
    CWE = "38899046"

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

    def create_description(self, parameter):
        """ Convierte los indices de un JSON a indices
            de Formstack """
        self.request_id \
            = parameter["data[id]"]
        self.data[self.CLASE] \
            = parameter["data[nivel]"]
        self.data[self.HALLAZGO] \
            = parameter["data[hallazgo]"]
        self.data[self.ESCENARIO] \
            = parameter["data[escenario]"]
        self.data[self.CARDINALIDAD] \
            = parameter["data[cardinalidad]"]
        self.data[self.ACTOR] \
            = parameter["data[actor]"]
        self.data[self.VULNERABILIDAD] \
            = parameter["data[vulnerabilidad]"]
        self.data[self.REQUISITOS] \
            = parameter["data[requisitos]"]
        self.data[self.DONDE] \
            = parameter["data[donde]"]
        self.data[self.SOLUCION_EFECTO] \
            = parameter["data[solucion_efecto]"]
        self.data[self.AMENAZA] \
            = parameter["data[amenaza]"]
        self.data[self.VECTOR_ATAQUE] \
            = parameter["data[vector_ataque]"]
        self.data[self.SISTEMA_COMPROMETIDO] \
            = parameter["data[sistema_comprometido]"]
        self.data[self.CWE] \
            = parameter["data[cwe]"]
        if self.data[self.CLASE] == "Detallado":
            self.data[self.CATEGORIA] \
                = parameter["data[categoria]"]
            self.data[self.VALOR_RIESGO] \
                = parameter["data[valor_riesgo]"]
            self.data[self.PROBABILIDAD] \
                = parameter["data[probabilidad]"]
            self.data[self.SEVERIDAD] \
                = parameter["data[severidad]"]

    def create_cssv2(self, parameter):
        """ Convierte los indices de un JSON a indices
            de Formstack """
        self.request_id \
            = parameter["data[id]"]
        self.data[self.VECTOR_ACCESO] \
            = parameter["data[vector_acceso]"]
        self.data[self.COMPLEJIDAD_ACCESO] \
            = parameter["data[complejidad_acceso]"]
        self.data[self.AUTENTICACION] \
            = parameter["data[autenticacion]"]
        self.data[self.EXPLOTABILIDAD] \
            = parameter["data[explotabilidad]"]
        self.data[self.CRITICIDAD] \
            = parameter["data[criticidad]"]
        self.data[self.IMPACTO_CONFIDENCIALIDAD] \
            = parameter["data[impacto_confidencialidad]"]
        self.data[self.IMPACTO_INTEGRIDAD] \
            = parameter["data[impacto_integridad]"]
        self.data[self.IMPACTO_DISPONIBILIDAD] \
            = parameter["data[impacto_disponibilidad]"]
        self.data[self.NIVEL_RESOLUCION] \
            = parameter["data[nivel_resolucion]"]
        self.data[self.NIVEL_CONFIANZA] \
            = parameter["data[nivel_confianza]"]

    def create_delete_set(self, parameter, analyst, project):
        """ Crea un set de datos para enviar en el correo
            de eliminacion de hallazgo """
        return {
            'mail_analista': analyst,
            'name_finding': parameter["vuln[hallazgo]"],
            'id_finding': parameter["vuln[id]"],
            'description': parameter["vuln[justificacion]"],
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


    def parse_description(self, request_arr): # noqa: C901
        "Convierte la descripcion de un hallazgo en formstack"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.HALLAZGO:
                self.data["hallazgo"] = finding["value"]
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
            if finding["field"] == self.CWE:
                try:
                    value = int(finding["value"])
                    urlbase = 'https://cwe.mitre.org/data/definitions/:id.html'
                    self.data["cwe"] = urlbase.replace(':id', str(value))
                except ValueError:
                    self.data["cwe"] = 'None'

    def parse_cssv2(self, request_arr):
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