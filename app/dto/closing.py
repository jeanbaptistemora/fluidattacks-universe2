""" DTO to map the Integrates fields to formstack """

class ClosingDTO(object):
    """ Class to create an object with the close attributes """

    PROYECT = '39596058'
    CYCLE = '50394892'
    FINDING = '39596063'
    VISIBLES = '47484630'
    REQUESTED = '39596365'
    VERIFIED = '47700230'
    OPENED = '39596368'
    WHICH_OPENED = '39596128'
    CLOSED = '39596370'
    WHICH_CLOSED = '39596202'

    def __init__(self):
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def parse(self, request):
        """ Converts a Formstack json into Integrates format  """
        self.data = dict()
        for closing in request["data"]:
            # DETALLES CIERRE
            if closing["field"] == self.FINDING:
                self.data["finding"] = closing["value"]
            if closing["field"] == self.VISIBLES:
                self.data["visibles"] = closing["value"]
            if closing["field"] == self.REQUESTED:
                self.data["requested"] = closing["value"]
            if closing["field"] == self.VERIFIED:
                self.data["verified"] = closing["value"]
            if closing["field"] == self.OPENED:
                self.data["opened"] = closing["value"]
            if closing["field"] == self.WHICH_OPENED:
                self.data["whichOpened"] = closing["value"]
            if closing["field"] == self.CLOSED:
                self.data["closed"] = closing["value"]
            if closing["field"] == self.WHICH_CLOSED:
                self.data["whichClosed"] = closing["value"]
            if closing["field"] == self.CYCLE:
                self.data["cycle"] = closing["value"]
        self.data["id"] = request["id"]
        self.data["timestamp"] = request["timestamp"]
        self.check_status()
        return self.data

    def check_status(self):
        """ Check the status of a finding based on
            its number of open vulnerabilities """
        state = 'Parcialmente cerrado'
        if self.data['visibles'] == self.data['requested']:
            if self.data['opened'] == '0':
                state = 'Cerrado'
            elif self.data['opened'] == self.data['visibles']:
                state = 'Abierto'
            elif int(self.data['opened']) > 0 and \
                 self.data['opened'] != self.data['visibles']:
                state = 'Parcialmente cerrado'
        self.data['estado'] = state
