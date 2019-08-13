from collections import OrderedDict

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt

from app.api.schema import SCHEMA


class FindingTests(TestCase):

    def test_get_finding(self):
        """ Check for finding """
        query = '''{
          finding(identifier: "422286126"){
            id
            vulnerabilities {
                findingId
                id
                historicState
                specific
                vulnType
                where
            }
          }
        }'''
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = "unittest"
        request.session['company'] = "unittest"
        request.session['role'] = "admin"
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        result = SCHEMA.execute(query, context_value=request)
        assert not result.errors
        assert result.data.get('finding')['id'] == '422286126'
        test_data = OrderedDict([
            ('findingId', '422286126'),
            ('id', u'80d6a69f-a376-46be-98cd-2fdedcffdcc0'),
            ('historicState',
             [{u'date': u'2018-09-28 10:32:58', u'state': u'open'},
              {u'date': u'2019-01-08 16:01:26', u'state': u'open'}]),
            ('specific', u'phone'),
            ('vulnType', u'inputs'),
            ('where', u'https://example.com')])
        assert test_data in result.data.get('finding')['vulnerabilities']
