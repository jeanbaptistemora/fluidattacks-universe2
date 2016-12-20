from django.test import TestCase
from app.models import FormstackAPI
# Create your tests here.

class FormstackAPITests(TestCase):

    def test_request(self):
        """ Realiza una peticion a formstack y verifica 
            que exista el key data en el json de respuesta """
        API = FormstackAPI()
        url = "https://www.formstack.com/api/v2/submission/293276999.json"
        request = API.request("GET", url)
        self.assertIs("data" in request, True)

    def test_get_submission(self):
        """ Prueba que se consulte correctamente una submission de formstack """
        API = FormstackAPI()
        submission_id = "293276999"
        request = API.get_submission(submission_id)
        self.assertEquals(request["id"], submission_id)

    def test_get_findings(self):
        API = FormstackAPI()
        project = "basaiti"
        request = API.get_findings(project)
        self.assertIs("submissions" in request, True)
    
    def test_get_eventualities(self):
        API = FormstackAPI()
        project = "basaiti"
        request = API.get_eventualities(project)
        self.assertIs("submissions" in request, True)

    def test_get_eventualities(self):
        API = FormstackAPI()
        project = "oka"
        request = API.get_order(project)
        self.assertIs("submissions" in request, True)

    def test_update_order(self):
        API = FormstackAPI()
        project = "Bramley"
        submission_id = "223360928"
        request = API.get_order(project, submission_id)
        self.assertIs("success" in request, True)

    def test_update_eventuality(self):
        API = FormstackAPI()
        afectacion = "0"
        submission_id = "244210431"
        request = API.get_order(project, submission_id)
        self.assertIs("success" in request, True)

    def test_update_finding(self):
        API = FormstackAPI()
        afectacion = "0"
        submission_id = "244210431"
        request = API.get_order(project, submission_id)
        self.assertIs("success" in request, True)