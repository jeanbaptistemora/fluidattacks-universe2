"""DTO para mapear los campos de integrates a formstack"""

class ClosingDTO(object):
    """ Clase para crear un objeto con los atributos de un cierre """

    PROYECTO = '39596058'
    CICLO = '50394892'
    HALLAZGO = '39596063'
    VISIBLES = '47484630'
    SOLICITADAS = '39596365'
    VERIFICADAS = '47700230'
    ABIERTAS = '39596368'
    ABIERTAS_CUALES = '39596128'
    CERRADAS = '39596370'
    CERRADAS_CUALES = '39596202'

    def __init__(self):
        """ Constructor de la clase """
        self.request_id = None
        self.data = dict()

    def parse(self, request):
        """Convierte los campos de un JSON 
           de Formstack para manipularlos en integrates."""
        self.data = dict()
        for closing in request["data"]:
            # DETALLES CIERRE
            if closing["field"] == self.HALLAZGO:
                self.data["hallazgo"] = closing["value"]
            if closing["field"] == self.VISIBLES:
                self.data["visibles"] = closing["value"]
            if closing["field"] == self.SOLICITADAS:
                self.data["solicitadas"] = closing["value"]
            if closing["field"] == self.VERIFICADAS:
                self.data["verificadas"] = closing["value"]
            if closing["field"] == self.ABIERTAS:
                self.data["abiertas"] = closing["value"]
            if closing["field"] == self.ABIERTAS_CUALES:
                self.data["abiertas_cuales"] = closing["value"]
            if closing["field"] == self.CERRADAS:
                self.data["cerradas"] = closing["value"]
            if closing["field"] == self.CERRADAS_CUALES:
                self.data["cerradas_cuales"] = closing["value"]
            if closing["field"] == self.CICLO:
                self.data["ciclo"] = closing["value"]
        self.data["id"] = request["id"]
        self.data["timestamp"] = request["timestamp"]
        self.check_status()
        return self.data

    def check_status(self):
        """ Verifica el estado de un hallazgo segun su calificacion """
        state = 'Parcialmente cerrado'
        if self.data['visibles'] == self.data['solicitadas']:
            if self.data['abiertas'] == '0':
                state = 'Cerrado'
            elif self.data['abiertas'] == self.data['visibles']:
                state = 'Abierto'
            elif int(self.data['abiertas']) > 0 and \
                 self.data['abiertas'] != self.data['visibles']:
                state = 'Parcialmente cerrado' 
        self.data['estado'] = state