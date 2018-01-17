"""DTO para mapear los campos de integrates a formstack"""
# pylint: disable=E0402
class ProjectDTO(object):
    """ Clase para crear un objeto con los atributos de un hallazgo """

    #Atributos proyecto
    PROYECTO_FLUID = "52601266"
    PROYECTO_CLIENTE = "60063920"
    CLIENTE = "52601817"
    CLASE = "52602145"
    LIDER = "52603216"
    ANALISTA = "53626289"
    ARQUITECTO = "60154418"
    FECHA_INICIO = "52601351"
    FECHA_FIN = "52601570"
    TIPO_PRUEBA = "52762210"
    AMBIENTE = "60063680"
    TIPO_COBERTURA = "60064178"
    COBERTURA = "60063976"
    TOE_CAMPOS_VISIBLES = "52762496"
    TOE_LINEAS_VISIBLES = "52762572"
    TOE_PUERTOS_VISIBLES = "52762526"
    TOE_CAMPOS_PROBADOS = "52762424"
    TOE_LINEAS_PROBADOS = "52602997"
    TOE_PUERTOS_PROBADOS = "52602989"
    IMPACTO_RELEVANTE = "60155980"
    OBSERVACIONES = "60063218"
    CONCLUSIONES = "60063227"
    TIPO_INDUSTRIA = "52765044"
    LENGUAJE = "52764314"
    TIPO_APLICACION = "52762843"
    INSUMOS = "60185565"
    CAMBIOS_AMBIENTE = "60185445"

    def __init__(self):
        """ Constructor de la clase """
        self.request_id = None
        self.data = dict()
    
    def parse(self, request_arr): # noqa: C901
        self.data["timestamp"] = request_arr["timestamp"]
        self.request_id = request_arr["id"]
        self.parse_general(request_arr)
        self.parse_coverage(request_arr)
        self.parse_resume(request_arr)
        return self.data

    def parse_general(self, request_arr): # noqa: C901
        "Convierte la descripcion de un hallazgo en formstack"
        for finding in request_arr["data"]:
            if finding["field"] == self.PROYECTO_FLUID:
                self.data["proyecto_fluid"] = finding["value"]
            if finding["field"] == self.PROYECTO_CLIENTE:
                self.data["proyecto_cliente"] = finding["value"]
            if finding["field"] == self.CLIENTE:
                self.data["cliente"] = finding["value"]
            if finding["field"] == self.CLASE:
                self.data["clase"] = finding["value"]
            if finding["field"] == self.LIDER:
                self.data["lider"] = finding["value"]
            if finding["field"] == self.ANALISTA:
                self.data["analista"] = finding["value"]
            if finding["field"] == self.ARQUITECTO:
                self.data["arquitecto"] = finding["value"]
            if finding["field"] == self.FECHA_INICIO:
                self.data["fecha_inicio"] = finding["value"]
            if finding["field"] == self.FECHA_FIN:
                self.data["fecha_fin"] = finding["value"]
            if finding["field"] == self.TIPO_PRUEBA:
                self.data["tipo_prueba"] = finding["value"]
            if finding["field"] == self.AMBIENTE:
                self.data["ambiente"] = finding["value"]
            if finding["field"] == self.CAMBIOS_AMBIENTE:
                self.data["cambios_ambiente"] = finding["value"]
            if finding["field"] == self.INSUMOS:
                self.data["insumos"] = finding["value"]

    def parse_coverage(self, request_arr): # noqa: C901
        "Convierte la cobertura de un hallazgo en proyecto"
        for finding in request_arr["data"]:
            if finding["field"] == self.TIPO_COBERTURA:
                self.data["tipo_cobertura"] = finding["value"]
            if finding["field"] == self.COBERTURA:
                self.data["cobertura"] = finding["value"]
            if finding["field"] == self.TOE_CAMPOS_VISIBLES:
                self.data["toe_campos_visibles"] = finding["value"]
            if finding["field"] == self.TOE_LINEAS_VISIBLES:
                self.data["toe_lineas_visibles"] = finding["value"]
            if finding["field"] == self.TOE_PUERTOS_VISIBLES:
                self.data["toe_puertos_visibles"] = finding["value"]
            if finding["field"] == self.TOE_CAMPOS_PROBADOS:
                self.data["toe_campos_probados"] = finding["value"]
            if finding["field"] == self.TOE_LINEAS_PROBADOS:
                self.data["toe_lineas_probadas"] = finding["value"]
            if finding["field"] == self.TOE_PUERTOS_PROBADOS:
                self.data["toe_puertos_probados"] = finding["value"]

    def parse_resume(self, request_arr): # noqa: C901
        "Convierte el resumen de un proyecto"
        for finding in request_arr["data"]:
            if finding["field"] == self.IMPACTO_RELEVANTE:
                self.data["impacto_relevate"] = finding["value"]
            if finding["field"] == self.OBSERVACIONES:
                self.data["observaciones"] = finding["value"]
            if finding["field"] == self.CONCLUSIONES:
                self.data["conclusiones"] = finding["value"]
            if finding["field"] == self.TIPO_INDUSTRIA:
                self.data["tipo_industria"] = finding["value"]
            if finding["field"] == self.LENGUAJE:
                self.data["lenguaje"] = finding["value"]
            if finding["field"] == self.TIPO_APLICACION:
                self.data["tipo_aplicacion"] = finding["value"]