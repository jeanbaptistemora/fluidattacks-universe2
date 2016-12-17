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