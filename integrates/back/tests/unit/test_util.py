import os
import pytest
import time
from collections import defaultdict
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Dict,
    List,
    Union,
)

import pytz
from boto3 import client
from graphql.language.ast import (
    ArgumentNode,
    FieldNode,
    NameNode,
    ObjectFieldNode,
    ValueNode,
    VariableNode,
)

from back import settings
from back.app.utils import create_user
from back.tests.unit.utils import (
    create_dummy_session,
    create_dummy_simple_session,
)
from backend.util import (
    assert_file_mime,
    calculate_hash_token,
    camelcase_to_snakecase,
    get_field_parameters,
    get_jwt_content,
    is_valid_format,
    iterate_s3_keys,
    list_to_dict,
    ord_asc_by_criticality,
    replace_all,
)
from custom_exceptions import ExpiredToken
from newutils import (
    datetime as datetime_utils,
    encodings,
    token as token_helper,
)
from redis_cluster.operations import (
    redis_del_entity_attr,
    redis_set_entity_attr,
)
from sessions import dal as sessions_dal
from users import domain as users_domain
from __init__ import (
    FI_AWS_S3_ACCESS_KEY,
    FI_AWS_S3_SECRET_KEY,
    FI_AWS_S3_BUCKET
)


pytestmark = [
    pytest.mark.asyncio,
]


def test_get_current_date():
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn)
    date = today.strftime('%Y-%m-%d %H:%M')
    test_data = datetime_utils.get_now_as_str()[:-3]
    assert isinstance(test_data, str)
    assert test_data == date


def test_ord_asc_by_criticality():
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

def test_assert_file_mime():
    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'mock/test-vulns.yaml')
    non_included_filename = os.path.join(path, 'mock/test.7z')
    allowed_mimes = ['text/plain']
    assert assert_file_mime(filename, allowed_mimes)
    assert not assert_file_mime(non_included_filename, allowed_mimes)

async def test_payload_encode_decode():
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    result = encodings.jwt_payload_decode(
        encodings.jwt_payload_encode(payload))
    assert payload == result

async def test_payload_encrypt_decrypt():
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    result = token_helper._decrypt_jwt_payload(
        token_helper._encrypt_jwt_payload(payload)
    )
    assert payload == result

async def test_decrypt_temp_support_for_nonencrypted():
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'iat': datetime.utcnow().timestamp(),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    result = token_helper._decrypt_jwt_payload(payload)
    assert payload == result

async def test_get_jwt_content():
    request = create_dummy_simple_session()
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    request.cookies[settings.JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity='session',
        attr='jti',
        email=payload['user_email'],
        value=payload['jti'],
        ttl=settings.SESSION_COOKIE_AGE
    )
    await redis_set_entity_attr(
        entity='session',
        attr='jwt',
        email=payload['user_email'],
        value=token,
        ttl=settings.SESSION_COOKIE_AGE
    )
    test_data = await get_jwt_content(request)
    expected_output = {
        u'user_email': u'unittest',
        u'exp': payload['exp'],
        u'sub': u'starlette_session',
        u'jti': payload['jti'],
    }
    assert test_data == expected_output

async def test_valid_token():
    request = create_dummy_simple_session()
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'session_token',
        'jti': calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    request.cookies[settings.JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
    await redis_set_entity_attr(
        entity='session',
        attr='jwt',
        email=payload['user_email'],
        value=token,
        ttl=settings.SESSION_COOKIE_AGE
    )
    test_data = await get_jwt_content(request)
    expected_output = {
        u'user_email': u'unittest',
        u'exp': payload['exp'],
        u'sub': u'session_token',
        u'jti': payload['jti'],
    }
    assert test_data == expected_output

async def test_valid_api_token():
    request = create_dummy_simple_session()
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'iat': datetime.utcnow().timestamp(),
        'sub': 'api_token',
        'jti': calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload, api=True)
    request.cookies[settings.JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
    await redis_set_entity_attr(
        entity='session',
        attr='jwt',
        email=payload['user_email'],
        value=token,
        ttl=settings.SESSION_COOKIE_AGE
    )
    test_data = await get_jwt_content(request)
    expected_output = {
        u'user_email': u'unittest',
        u'exp': payload['exp'],
        u'iat': payload['iat'],
        u'sub': u'api_token',
        u'jti': payload['jti'],
    }
    assert test_data == expected_output

async def test_expired_token():
    request = create_dummy_simple_session()
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    request.cookies[settings.JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity='session',
        attr='jti',
        email=payload['user_email'],
        value=payload['jti'],
        ttl=5
    )
    time.sleep(6)
    with pytest.raises(ExpiredToken):
        assert await get_jwt_content(request)


async def test_token_expired():
    """Check if after change jti exception is raised."""
    user_email = 'integratesuser@gmail.com'
    request = await create_dummy_session(user_email)
    setattr(request, 'store', defaultdict(lambda: None))
    assert await get_jwt_content(request)

    new_request = await create_dummy_session(user_email)
    setattr(new_request, 'store', defaultdict(lambda: None))
    assert await get_jwt_content(new_request)

    with pytest.raises(ExpiredToken):
        setattr(request, 'store', defaultdict(lambda: None))
        assert await get_jwt_content(request)

    setattr(new_request, 'store', defaultdict(lambda: None))
    assert await get_jwt_content(new_request)


async def test_revoked_token():
    request = create_dummy_simple_session()
    payload = {
        'user_email': 'unittest',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'starlette_session',
        'jti': calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    request.cookies[settings.JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity='session',
        attr='jti',
        email=payload['user_email'],
        value=payload['jti'],
        ttl=settings.SESSION_COOKIE_AGE
    )
    await redis_del_entity_attr(
        entity='session',
        attr='jti',
        email=payload['user_email']
    )
    with pytest.raises(ExpiredToken):
        assert await get_jwt_content(request)

def test_iterate_s3_keys():
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

def test_replace_all():
    data = {'a': 'a', 'b': 'b', 'c': 'c'}
    text = 'replaced'
    test_data = replace_all(text, data)
    expected_output = 'replaced'
    assert test_data == expected_output

def test_list_to_dict():
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

def test_camelcase_to_snakecase():
    camelcase_string = 'thisIsATest'
    test_data = camelcase_to_snakecase(camelcase_string)
    expected_output = 'this_is_a_test'
    assert test_data == expected_output

def test_is_valid_format():
    date = '2019-03-30 00:00:00'
    invalid_date = '2019/03/30 00:00:00'
    assert is_valid_format(date)
    assert not is_valid_format(invalid_date)

def test_get_field_parameters__with_arguments__regression():
    field_node = FieldNode(
        kind='Field',
        name=NameNode(
            kind='Name',
            value='Test'
        ),
        arguments=[
            ArgumentNode(
                kind='Argument',
                name=NameNode(
                    kind='Name',
                    value='id'
                ),
                value=NameNode(
                    kind='StringValue',
                    value='user-1'
                )
            ),
            ArgumentNode(
                kind='Argument',
                name=NameNode(
                    kind='Name',
                    value='currentTestingUniverse'
                ),
                value=NameNode(
                    kind='StringValue',
                    value='C-137'
                )
            )
        ]
    )

    assert ({'id':'user-1', 'current_testing_universe':'C-137'} ==
            get_field_parameters(field_node))

@pytest.mark.xfail(reason='from commit 1b77937f on it\'s returning {}')
def test_get_field_parameters__without_arguments__regression():
    field_node = FieldNode(
        kind='Field',
        name=NameNode(
            kind='Name',
            value='Test'
        ),
        arguments=[]
    )

    assert None == get_field_parameters(field_node)

def test_get_field_parameters__with_an_argument_without_value__regression():
    field_node = FieldNode(
        kind='Field',
        name=NameNode(
            kind='Name',
            value='Test'
        ),
        arguments=[
            ArgumentNode(
                kind='Argument',
                name=NameNode(
                    kind='Name',
                    value='id'
                ),
                value=NameNode(
                    kind='StringValue',
                    value='user-1'
                )
            ),
            ArgumentNode(
                kind='Argument',
                name=NameNode(
                    kind='Name',
                    value='currentTestingUniverse'
                ),
                value=VariableNode(
                    name=NameNode(
                        kind='StringValue',
                        value='universe'
                    )
                )
            )
        ]
    )

    assert ({'id':'user-1', 'current_testing_universe':None} ==
            get_field_parameters(field_node))
    assert ({'id':'user-1', 'current_testing_universe':'unkwon'} ==
            get_field_parameters(field_node, {'universe':'unkwon'}))

@pytest.mark.xfail(
    reason='from commit 01669ab2 on it\'s returning {\'id\': ValueNode}'
)
def test_get_field_parameters__argument_with_fieldnode_as_value__regression():
    field_node = FieldNode(
        kind='Field',
        name=NameNode(
            kind='Name',
            value='Test'
        ),
        arguments=[
            ArgumentNode(
                kind='Argument',
                name=NameNode(
                    kind='Name',
                    value='id'
                ),
                value=ObjectFieldNode(
                    kind='StringValue',
                    name=NameNode(
                        kind='Name',
                        value='id'
                    ),
                    value=ValueNode()
                )
            )
        ]
    )

    assert {} == get_field_parameters(field_node)


@pytest.mark.changes_db
async def test_create_user():
    timezone = pytz.timezone(settings.TIME_ZONE)

    async def get_user_attrs(
        email: str,
        attrs: List[str]
    ) -> Dict[str, Union[str, datetime]]:
        user_attrs = await users_domain.get_attributes(email, attrs)
        if 'last_login' in user_attrs:
            user_attrs['last_login'] = timezone.localize(
                datetime.strptime(
                    user_attrs['last_login'],
                    '%Y-%m-%d %H:%M:%S'
                )
            )
        return user_attrs

    now: datetime = datetime.now(tz=timezone)
    email: str = 'integratescustomer@fluidattacks.com'
    user_info = await get_user_attrs(email, ['registered', 'last_login'])
    assert user_info['registered']
    assert user_info['last_login'] < now

    time.sleep(1)
    await create_user({'email': email})
    user_info = await get_user_attrs(email, ['last_login'])
    assert user_info['last_login'] > now
