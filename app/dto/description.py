"""DTO para mapear los campos de integrates a formstack"""

class DescriptionDTO(object):
    """ Clase para crear un objeto con los atributos descriptivos """

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

    def __init__(self):
        """ Constructor de la clase """
        self.request_id = None
        self.data = dict()

    def create(self, parameter):
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
        self.to_formstack()

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data