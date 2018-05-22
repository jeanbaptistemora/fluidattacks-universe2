"""DTO para mapear los campos de integrates a formstack"""

class EventualityDTO(object):
    """ Clase para crear un objeto con los atributos cssv2 """

    ANALIST = "29042426"
    CLIENT = "29042288"
    FLUID_PROJECT = "29042322"
    CLIENT_PROJECT = "39595967"
    TIPO = "29042327"
    DETALLE = "29042402"
    FECHA = "29042174"
    ESTADO = "29062640"
    AFECTACION = "29042542"

    def __init__(self):
        """ Constructor de la clase """
        self.request_id = None
        self.data = dict()

    def create(self, parameter):
        """ Convierte los indices de un JSON a indices
            de Formstack """
        if "vuln[id]" in parameter:
            self.request_id \
                = parameter["vuln[id]"]
        if "vuln[affectation]" in parameter:
            self.data[self.AFECTACION] \
                = parameter["vuln[affectation]"]
        if "vuln[fluidProject]" in parameter:
            self.data[self.FLUID_PROJECT] \
                = parameter["vuln[fluidProject]"]
        if "vuln[affectation]" in parameter:
            if parameter["vuln[affectation]"] != "":
                self.data[self.ESTADO] \
                    = "Tratada"
        self.to_formstack()

    def parse(self, submission_id, request_arr):
        self.data = dict()
        self.data["id"] = submission_id
        for row in request_arr["data"]:
            if row["field"] == self.ANALIST:
                self.data["analyst"] = row["value"]
            if row["field"] == self.CLIENT:
                self.data["client"] = row["value"]
            if row["field"] == self.FLUID_PROJECT:
                self.data["fluidProject"] = row["value"]
            if row["field"] == self.CLIENT_PROJECT:
                self.data["clientProject"] = row["value"]
            if row["field"] == self.TIPO:
                self.data["tipo"] = row["value"]
            if row["field"] == self.DETALLE:
                self.data["detalle"] = row["value"]
            if row["field"] == self.FECHA:
                self.data["fecha"] = row["value"]
            if row["field"] == self.ESTADO:
                self.data["estado"] = row["value"]
            if row["field"] == self.AFECTACION:
                self.data["affectation"] = row["value"]
        return self.data

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data
