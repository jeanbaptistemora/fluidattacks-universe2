"""DTO para mapear los campos de integrates a formstack"""

class Cssv2DTO(object):
    """ Clase para crear un objeto con los atributos cssv2 """
    
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
        self.to_formstack()

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data