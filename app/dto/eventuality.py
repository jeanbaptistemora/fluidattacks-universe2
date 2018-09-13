""" DTO to map the Integrates fields to formstack """

class EventualityDTO(object):
    """ Class to create an object with the CSSV2 attributes """

    ANALIST = "29042426"
    CLIENT = "29042288"
    FLUID_PROJECT = "29042322"
    CLIENT_PROJECT = "39595967"
    TYPE = "29042327"
    DETAIL = "29042402"
    DATE = "29042174"
    STATUS = "29062640"
    AFFECTATION = "29042542"
    EVIDENCE = "29042411"
    ACCESSIBILITY = "57917686"
    AFFECTED_COMPONENTS = "52661157"

    def __init__(self):
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def create(self, parameter):
        """ Converts the index of a JSON to Formstack index """
        if "vuln[id]" in parameter:
            self.request_id \
                = parameter["vuln[id]"]
        if "vuln[affectation]" in parameter:
            self.data[self.AFFECTATION] \
                = parameter["vuln[affectation]"]
        if "vuln[fluidProject]" in parameter:
            self.data[self.FLUID_PROJECT] \
                = parameter["vuln[fluidProject]"]
        if "vuln[affectation]" in parameter:
            if parameter["vuln[affectation]"] != "":
                self.data[self.STATUS] \
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
            if row["field"] == self.TYPE:
                self.data["type"] = row["value"]
            if row["field"] == self.DETAIL:
                self.data["detalle"] = row["value"]
            if row["field"] == self.DATE:
                self.data["fecha"] = row["value"]
            if row["field"] == self.STATUS:
                self.data["estado"] = row["value"]
            if row["field"] == self.AFFECTATION:
                self.data["affectation"] = row["value"]
            if row["field"] == self.EVIDENCE:
                self.data["evidence"] = row["value"]
            if row["field"] == self.ACCESSIBILITY:
                self.data["accessibility"] = row["value"]
            if row["field"] == self.AFFECTED_COMPONENTS:
                self.data["affectedComponents"] = row["value"]
        return self.data

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data
