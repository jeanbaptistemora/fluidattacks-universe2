""" DTO to map the Integrates fields to formstack """
import base64

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
    INTERESTED_CUSTOMER = '39596055'
    CUSTOMER_CODE = '39597296'
    WHERE = '39596328'
    EXPLOIT = '52862857'
    OPEN_EVIDENCE = '39596152'
    CLOSE_EVIDENCE = '39596215'

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

    def mask_closing(self, closingid, mask_value):
        """Mask closing."""
        self.request_id = closingid
        self.data[self.INTERESTED_CUSTOMER] = mask_value
        self.data[self.CUSTOMER_CODE] = mask_value
        self.data[self.WHERE] = mask_value
        self.data[self.EXPLOIT] = base64.b64encode(mask_value)
        self.data[self.WHICH_OPENED] = mask_value
        self.data[self.OPEN_EVIDENCE] = base64.b64encode(mask_value)
        self.data[self.WHICH_CLOSED] = mask_value
        self.data[self.CLOSE_EVIDENCE] = base64.b64encode(mask_value)

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_" + key] = value
        self.data = new_data
