from __future__ import absolute_import
import os
import time
import pytest
from datetime import datetime, timedelta

from boto3 import client
from django.http import JsonResponse
from django.test import TestCase
from django.test import RequestFactory
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from jose import jwt
from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
)
import json

from backend.exceptions import ExpiredToken
from backend.util import (
    response, ord_asc_by_criticality,
    assert_file_mime, has_release, get_last_vuln, validate_release_date,
    get_jwt_content, iterate_s3_keys, replace_all,
    list_to_dict, camelcase_to_snakecase, is_valid_format,
    calculate_hash_token, remove_token, save_token
)

from backend.dal.finding import get_finding
from test_async.utils import create_dummy_simple_session

pytestmark = [
    pytest.mark.asyncio,
]


class UtilTests(TestCase):

    def test_response(self):
        data = 'this is data'
        message = 'this is a test'
        error = '500'
        test_data = response(data, message, error)
        expected_output = { 'data': 'this is data',
                            'message': 'this is a test',
                            'error': '500'}
        assert json.loads(test_data.content.decode('utf-8')) == expected_output

    def test_ord_asc_by_criticality(self):
        sortable_data = [
            {'severityCvss': 40}, {'severityCvss': 13}, {'severityCvss': 20},
            {'severityCvss': 30}, {'severityCvss': 12}, {'severityCvss': 1},
            {'severityCvss': 54}
        ]
        test_data = ord_asc_by_criticality(sortable_data)
        expected_output = [
            {'severityCvss': 54}, {'severityCvss': 40}, {'severityCvss': 30},
            {'severityCvss': 20}, {'severityCvss': 13}, {'severityCvss': 12},
            {'severityCvss': 1}]
        assert test_data == expected_output

    def test_assert_file_mime(self):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, 'mock/test-vulns.yaml')
        non_included_filename = os.path.join(path, 'mock/test.7z')
        allowed_mimes = ['text/plain']
        assert assert_file_mime(filename, allowed_mimes)
        assert not assert_file_mime(non_included_filename, allowed_mimes)

    def test_has_release(self):
        test_dict = {'releaseDate': 'date'}
        test_dict_with_no_release_date = {'noReleaseDate': 'date'}
        assert has_release(test_dict)
        assert not has_release(test_dict_with_no_release_date)

    async def test_get_last_vuln(self):
        finding = await get_finding('422286126')
        test_data = get_last_vuln(finding)
        expected_output = datetime(2018, 7, 9).date()
        assert test_data == expected_output

    async def test_validate_release_date(self):
        finding = await get_finding('422286126')
        unreleased_finding = await get_finding('560175507')
        assert validate_release_date(finding)
        assert not validate_release_date(unreleased_finding)

    def test_get_jwt_content(self):
        request = create_dummy_simple_session()
        payload = {
            'user_email': 'unittest',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
        test_data = get_jwt_content(request)
        expected_output = {
            u'company': u'unittest',
            u'user_email': u'unittest',
            u'exp': payload['exp'],
            u'sub': u'django_session',
            u'jti': payload['jti'],
        }
        assert test_data == expected_output

    def test_valid_token(self):
        request = create_dummy_simple_session()
        payload = {
            'user_email': 'unittest',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'session_token',
            'jti': calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
        test_data = get_jwt_content(request)
        expected_output = {
            u'company': u'unittest',
            u'user_email': u'unittest',
            u'exp': payload['exp'],
            u'sub': u'session_token',
            u'jti': payload['jti'],
        }
        assert test_data == expected_output

    def test_valid_api_token(self):
        request = create_dummy_simple_session()
        payload = {
            'user_email': 'unittest',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'iat': datetime.utcnow().timestamp(),
            'sub': 'api_token',
            'jti': calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET_API,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
        test_data = get_jwt_content(request)
        expected_output = {
            u'company': u'unittest',
            u'user_email': u'unittest',
            u'exp': payload['exp'],
            u'iat': payload['iat'],
            u'sub': u'api_token',
            u'jti': payload['jti'],
        }
        assert test_data == expected_output

    def test_expired_token(self):
        request = create_dummy_simple_session()
        payload = {
            'user_email': 'unittest',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        save_token(f'fi_jwt:{payload["jti"]}', token, 5)
        time.sleep(6)
        with pytest.raises(ExpiredToken):
            assert get_jwt_content(request)

    def test_revoked_token(self):
        request = create_dummy_simple_session()        
        payload = {
            'user_email': 'unittest',
            'company': 'unittest',
            'exp': datetime.utcnow() +
            timedelta(seconds=settings.SESSION_COOKIE_AGE),
            'sub': 'django_session',
            'jti': calculate_hash_token()['jti'],
        }
        token = jwt.encode(
            payload,
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        redis_token_name = f'fi_jwt:{payload["jti"]}'
        save_token(redis_token_name, token, settings.SESSION_COOKIE_AGE + (20 * 60))
        remove_token(redis_token_name)
        with pytest.raises(ExpiredToken):
            assert get_jwt_content(request)

    def test_iterate_s3_keys(self):
        s3_client = client(
            service_name='s3',
            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
            aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))
        bucket = FI_AWS_S3_BUCKET
        key = 'oneshottest'
        test_data = list(iterate_s3_keys(s3_client, bucket, key))
        assert isinstance(test_data, list)
        for item in test_data:
            assert key in item

    def test_replace_all(self):
        data = {'a': 'a', 'b': 'b', 'c': 'c'}
        text = 'replaced'
        test_data = replace_all(text, data)
        expected_output = 'replaced'
        assert test_data == expected_output

    def test_list_to_dict(self):
        keys = ['item', 'item2', 'item3']
        values = ['hi', 'this is a', 'item']
        test_data = list_to_dict(keys, values)
        expected_output = {'item': 'hi', 'item2': 'this is a', 'item3': 'item'}
        second_test_data = list_to_dict(keys[0:2], values)
        second_expected_output = {'item': 'hi', 'item2': 'this is a', 2: 'item'}
        third_test_data = list_to_dict(keys, values[0:2])
        third_expected_output = {'item': 'hi', 'item2': 'this is a', 'item3': ''}
        assert test_data == expected_output
        assert second_test_data == second_expected_output
        assert third_test_data == third_expected_output

    def test_camelcase_to_snakecase(self):
        camelcase_string = 'thisIsATest'
        test_data = camelcase_to_snakecase(camelcase_string)
        expected_output = 'this_is_a_test'
        assert test_data == expected_output

    def test_is_valid_format(self):
        date = '2019-03-30 00:00:00'
        invalid_date = '2019/03/30 00:00:00'
        assert is_valid_format(date)
        assert not is_valid_format(invalid_date)
