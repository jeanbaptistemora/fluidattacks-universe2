from django.test import TestCase

from app.dal.helpers.formstack import FormstackAPI


class FormstackAPITests(TestCase):
    def test_request(self):
        """ Make a request to formstack and verify that
            the key data exists in the response json. """
        api_frms = FormstackAPI()
        url = 'https://www.formstack.com/api/v2/submission/293276999.json'
        request = api_frms.request('GET', url)
        assert 'data' in request

    def test_get_submission(self):
        """ Check that Formstack correctly return a submission query. """
        api_frms = FormstackAPI()
        submission_id = '293276999'
        request = api_frms.get_submission(submission_id)
        assert request['id'] == submission_id
