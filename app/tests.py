from django.test import TestCase
from .api.formstack import FormstackAPI
from .entity.query import Query
from graphene import Schema
# Create your tests here.


class FormstackAPITests(TestCase):
    def test_request(self):
        """ Make a request to formstack and verify that
            the key data exists in the response json. """
        api_frms = FormstackAPI()
        url = "https://www.formstack.com/api/v2/submission/293276999.json"
        request = api_frms.request("GET", url)
        self.assertIs("data" in request, True)

    def test_get_submission(self):
        """ Check that Formstack correctly return a submission query. """
        api_frms = FormstackAPI()
        submission_id = "293276999"
        request = api_frms.get_submission(submission_id)
        self.assertEquals(request["id"], submission_id)

    def test_get_findings(self):
        """ Check that Formstack correctly return the findings of a project. """
        api_frms = FormstackAPI()
        project = "basaiti"
        request = api_frms.get_findings(project)
        self.assertIs("submissions" in request, True)

    def test_get_eventualities(self):
        """ Check that Formstack correctly return
            the eventualities of a project. """
        api_frms = FormstackAPI()
        project = "basaiti"
        request = api_frms.get_eventualities(project)
        self.assertIs("submissions" in request, True)

    def test_update_eventuality(self):
        """Check that an eventuality update request works correctly."""
        api_frms = FormstackAPI()
        affectation = "0"
        submission_id = "244210431"
        data = {
            "29042542": affectation
        }
        request = api_frms.update(submission_id, data)
        self.assertIs("success" in request, True)

class GraphQLTests(TestCase):

    def test_get_alert(self):
        """Check for project alert"""
        query = """{
            alert(project:"bwapp", organization:"testing"){
                message
            }
        }"""
        schema = Schema(query=Query)
        result = schema.execute(query)
        if "alert" in result.data:
            message = result.data["alert"]["message"]
            self.assertIs(
                message == "Alerta de prueba unitaria",
                True
            )
        self.assertFalse("alert" not in result.data)