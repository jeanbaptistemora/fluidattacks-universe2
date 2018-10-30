import json
from collections import OrderedDict

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt

from .api.formstack import FormstackAPI
from .entity import schema

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
            alert(projectName:"unittesting", organization:"fluid"){
                message
            }
        }"""
        request = RequestFactory().get('/')
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': "unittest",
              'user_role': "admin"
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = schema.schema.execute(query, context_value=request)
        if "alert" in result.data:
            message = result.data["alert"]["message"]
            self.assertIs(
                message == "unittest",
                True
            )
        self.assertFalse("alert" not in result.data)

    def test_get_event(self):
        """Check for eventuality"""
        query = """{
            event(identifier:"418900971"){
                detail
            }
        }"""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['access'] = {'unittesting': [422286126, 436423161, 435326633, 435326463, 418900971]}
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': 'unittest',
              'user_role': 'admin'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = dict(schema.schema.execute(query, context_value=request).data)
        if "event" in result.keys():
            detail = dict(result["event"])["detail"]
            self.assertIs(
                detail == "Integrates unit test ",
                True
            )
        self.assertFalse("event" not in result)

    def test_get_events(self):
        """Check for eventualities"""
        query = """{
            events(projectName:"unittesting"){
                detail
            }
        }"""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['access'] = {"unittesting": ["422286126", "436423161", "435326633", "435326463", "418900971"]}
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': 'unittest',
              'user_role': 'admin'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = dict(schema.schema.execute(query, context_value=request).data)
        if "events" in result:
            detail = dict(result["events"][0])["detail"]
            self.assertIs(
                len(detail) >= 1,
                True
            )
        self.assertFalse("events" not in result)

    def test_get_finding(self):
        """ Check for finding """
        query = """{
          finding(identifier: "422286126"){
            id
            success
            errorMessage
            vulnerabilities {
                findingId
                id
                historicState
                specific
                vulnType
                where
            }
          }
        }"""
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.session['access'] = {"unittesting": [
            "422286126", "436423161",
            "435326633", "435326463",
            "418900971"
            ]}
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': 'unittest',
              'user_role': 'admin'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = schema.schema.execute(query, context_value=request)
        assert not result.errors
        self.assertEqual(result.data.get("finding")["id"], '422286126')
        test_data = OrderedDict([
            ('findingId', '422286126'),
            ('id', u'80d6a69f-a376-46be-98cd-2fdedcffdcc0'),
            ('historicState',
                [{u'date': u'2018-09-28 10:32:58', u'state': u'open'}]),
            ('specific', u'phone'),
            ('vulnType', u'inputs'),
            ('where', u'https://example.com')])
        assert test_data in result.data.get("finding")["vulnerabilities"]

    def test_get_resources(self):
        """ Check for project resources """
        query = """{
          resources(projectName: "unittesting"){
            repositories
            environments
          }
        }"""
        request = RequestFactory().get('/')
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': "unittest",
              'user_role': "admin"
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = schema.schema.execute(query, context_value=request)
        assert not result.errors
        self.assertTrue("https://gitlab.com/fluidsignal/engineering/" in \
                        result.data.get("resources")["repositories"])
        self.assertTrue("https://fluidattacks.com/" in \
                        result.data.get("resources")["environments"])

    def test_add_resources(self):
        """ Check for add project resources"""
        reposToAdd = [
            {"branch": "master", "repository": "https://gitlab.com/fluidsignal/unittest"}
        ]
        envsToAdd = [
            {"environment": "https://unittesting.fluidattacks.com/"},
        ]
        query = """mutation {
          addRepositories(projectName: "unittesting", resourcesData: "$repos") {
            success
          }
          addEnvironments(projectName: "unittesting", resourcesData: "$envs") {
            success
          }
        }"""
        query = query.replace("$repos", json.dumps(reposToAdd).replace('"', '\\"'))
        query = query.replace("$envs", json.dumps(envsToAdd).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.session['access'] = {"unittesting": [
            "422286126", "436423161",
            "435326633", "435326463",
            "418900971"
            ]}
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': "unittest",
              'user_role': "admin"
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = schema.schema.execute(query, context_value=request)
        assert not result.errors
        self.assertTrue(result.data.get("addRepositories")["success"])
        self.assertTrue(result.data.get("addEnvironments")["success"])

    def test_remove_resources(self):
        """ Check for remove project resources """
        repoToRemove = {"branch": "master", "urlRepo": "https://gitlab.com/fluidsignal/unittest"}
        envToRemove = {"urlEnv": "https://unittesting.fluidattacks.com/"}
        query = """mutation{
          removeRepositories(projectName: "unittesting", repositoryData: "$repo"){
            success
          }
          removeEnvironments(projectName: "unittesting", repositoryData: "$env"){
            success
          }
        }"""
        query = query.replace("$repo", json.dumps(repoToRemove).replace('"', '\\"'))
        query = query.replace("$env", json.dumps(envToRemove).replace('"', '\\"'))
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.session['access'] = {"unittesting": [
            "422286126", "436423161",
            "435326633", "435326463",
            "418900971"
            ]}
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
              'user_email': "unittest",
              'user_role': "admin"
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = schema.schema.execute(query, context_value=request)
        assert not result.errors
        self.assertTrue(result.data.get("removeRepositories")["success"])
        self.assertTrue(result.data.get("removeEnvironments")["success"])
