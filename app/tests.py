from django.test import TestCase
from app.models import FormstackAPI
from fluidasserts.helper import http_helper
from fluidasserts.service import http
# Create your tests here.


class FormstackAPITests(TestCase):
    def test_request(self):
        """Realiza una peticion a formstack y verifica
        que exista el key data en el json de respuesta."""
        api_frms = FormstackAPI()
        url = "https://www.formstack.com/api/v2/submission/293276999.json"
        request = api_frms.request("GET", url)
        self.assertIs("data" in request, True)

    def test_get_submission(self):
        """Prueba que se consulte correctamente una submission de
        formstack."""
        api_frms = FormstackAPI()
        submission_id = "293276999"
        request = api_frms.get_submission(submission_id)
        self.assertEquals(request["id"], submission_id)

    def test_get_findings(self):
        """Prueba que se consulte correctamente los hallazgos de un
        proyecto."""
        api_frms = FormstackAPI()
        project = "basaiti"
        request = api_frms.get_findings(project)
        self.assertIs("submissions" in request, True)

    def test_get_eventualities(self):
        """Prueba que se consulte correctamente las eventualidades de
        un proyecto."""
        api_frms = FormstackAPI()
        project = "basaiti"
        request = api_frms.get_eventualities(project)
        self.assertIs("submissions" in request, True)

    def test_get_order(self):
        """Obtiene el pedido de un nombre de proyecto."""
        api_frms = FormstackAPI()
        project = "Hayes"
        request = api_frms.get_order(project)
        self.assertIs("submissions" in request, True)

    def test_update_order(self):
        """Actualiza un pedido en Formstack."""
        api_frms = FormstackAPI()
        project = "Bramley"
        submission_id = "244210431"
        request = api_frms.update_order(project, submission_id)
        self.assertIs("success" in request, True)

    def test_update_eventuality(self):
        """Actualiza la afectacion de una eventualidad en Formstack."""
        api_frms = FormstackAPI()
        afectacion = "0"
        submission_id = "244210431"
        request = api_frms.update_eventuality(afectacion, submission_id)
        self.assertIs("success" in request, True)

    def test_login(self):
        """Log in to integrates."""
        login_url = 'http://localhost/login'
        http_session = http_helper.HTTPSession(login_url)

        http_session.data = \
            'user=customer%40bancolombia.com.co&\
pass=jpwtwvk4p8c'

        successful_text = 'Bienvenido customer@bancolombia'
        http_session.formauth_by_response(successful_text)
        self.assertIs(http_session.is_auth, True)

    def get_integrates_cookies(self):
        """Log in to integrates and return valid cookie."""
        login_url = 'http://localhost/login'
        http_session = http_helper.HTTPSession(login_url)

        http_session.data = \
            'user=customer%40bancolombia.com.co&\
pass=jpwtwvk4p8c'

        successful_text = 'Bienvenido customer@bancolombia'
        http_session.formauth_by_response(successful_text)

        if not http_session.is_auth:
            return {}
        return http_session.cookies

    def search_project(self):
        """Perform a project search in integrates."""

        url = 'http://localhost/get_findings?project=HAYES'
        cookies = self.get_integrates_cookies()
        success_text = 'Se generan sentencias SQL'
        http_session = http_helper.HTTPSession(url, cookies=cookies)
        self.assertIs(success_text in http_session.response.text, True)
