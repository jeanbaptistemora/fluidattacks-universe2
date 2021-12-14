# pylint: disable=protected-access
from api.mutations.sign_in import (
    log_user_in,
)
from back.tests.unit.utils import (
    create_dummy_session,
    create_dummy_simple_session,
)
from collections import (
    defaultdict,
)
from custom_exceptions import (
    ExpiredToken,
)
from datetime import (
    datetime,
    timedelta,
)
from newutils import (
    datetime as datetime_utils,
    encodings,
    files as files_utils,
    token as token_utils,
    utils,
)
import os
import pytest
import pytz  # type: ignore
from redis_cluster.operations import (
    redis_del_entity_attr,
    redis_set_entity_attr,
)
from sessions import (
    dal as sessions_dal,
)
from settings import (
    JWT_COOKIE_NAME,
    SESSION_COOKIE_AGE,
    TIME_ZONE,
)
import time
from typing import (
    Dict,
    List,
    Union,
)
from users import (
    domain as users_domain,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_get_current_date() -> None:
    tzn = pytz.timezone(TIME_ZONE)
    today = datetime.now(tz=tzn)
    date = today.strftime("%Y-%m-%d %H:%M")
    test_data = datetime_utils.get_now_as_str()[:-3]
    assert isinstance(test_data, str)
    assert test_data == date


def test_assert_file_mime() -> None:
    path = os.path.dirname(__file__)
    filename = os.path.join(path, "mock/test-vulns.yaml")
    non_included_filename = os.path.join(path, "mock/test.7z")
    allowed_mimes = ["text/plain"]
    assert files_utils.assert_file_mime(filename, allowed_mimes)
    assert not files_utils.assert_file_mime(
        non_included_filename, allowed_mimes
    )


async def test_payload_encode_decode() -> None:
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    result = encodings.jwt_payload_decode(
        encodings.jwt_payload_encode(payload)
    )
    assert payload == result


async def test_payload_encrypt_decrypt() -> None:
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    result = token_utils._decrypt_jwt_payload(
        token_utils._encrypt_jwt_payload(payload)
    )
    assert payload == result


async def test_decrypt_temp_support_for_nonencrypted() -> None:
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "iat": datetime.utcnow().timestamp(),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    result = token_utils._decrypt_jwt_payload(payload)
    assert payload == result


async def test_get_jwt_content() -> None:
    request = create_dummy_simple_session()
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],
        value=payload["jti"],
        ttl=SESSION_COOKIE_AGE,
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],
        value=token,
        ttl=SESSION_COOKIE_AGE,
    )
    test_data = await token_utils.get_jwt_content(request)
    expected_output = {
        "user_email": "unittest",
        "exp": payload["exp"],
        "sub": "starlette_session",
        "jti": payload["jti"],
    }
    assert test_data == expected_output


async def test_valid_token() -> None:
    request = create_dummy_simple_session()
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "session_token",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(
        f'fi_jwt:{payload["jti"]}', token, SESSION_COOKIE_AGE
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],
        value=token,
        ttl=SESSION_COOKIE_AGE,
    )
    test_data = await token_utils.get_jwt_content(request)
    expected_output = {
        "user_email": "unittest",
        "exp": payload["exp"],
        "sub": "session_token",
        "jti": payload["jti"],
    }
    assert test_data == expected_output


async def test_valid_api_token() -> None:
    request = create_dummy_simple_session()
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "iat": datetime.utcnow().timestamp(),
        "sub": "api_token",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload, api=True)
    request.cookies[JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(
        f'fi_jwt:{payload["jti"]}', token, SESSION_COOKIE_AGE
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],
        value=token,
        ttl=SESSION_COOKIE_AGE,
    )
    test_data = await token_utils.get_jwt_content(request)
    expected_output = {
        "user_email": "unittest",
        "exp": payload["exp"],
        "iat": payload["iat"],
        "sub": "api_token",
        "jti": payload["jti"],
    }
    assert test_data == expected_output


async def test_expired_token() -> None:
    request = create_dummy_simple_session()
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],
        value=payload["jti"],
        ttl=5,
    )
    time.sleep(6)
    with pytest.raises(ExpiredToken):
        assert await token_utils.get_jwt_content(request)


async def test_token_expired() -> None:
    user_email = "integratesuser@gmail.com"
    request = await create_dummy_session(user_email)
    setattr(request, "store", defaultdict(lambda: None))
    assert await token_utils.get_jwt_content(request)

    new_request = await create_dummy_session(user_email)
    setattr(new_request, "store", defaultdict(lambda: None))
    assert await token_utils.get_jwt_content(new_request)

    with pytest.raises(ExpiredToken):
        setattr(request, "store", defaultdict(lambda: None))
        assert await token_utils.get_jwt_content(request)

    setattr(new_request, "store", defaultdict(lambda: None))
    assert await token_utils.get_jwt_content(new_request)


async def test_revoked_token() -> None:
    request = create_dummy_simple_session()
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],
        value=payload["jti"],
        ttl=SESSION_COOKIE_AGE,
    )
    await redis_del_entity_attr(
        entity="session", attr="jti", email=payload["user_email"]
    )
    with pytest.raises(ExpiredToken):
        assert await token_utils.get_jwt_content(request)


def test_replace_all() -> None:
    data = {"a": "a", "b": "b", "c": "c"}
    text = "replaced"
    test_data = utils.replace_all(text, data)
    expected_output = "replaced"
    assert test_data == expected_output


def test_list_to_dict() -> None:
    keys = ["item", "item2", "item3"]
    values = ["hi", "this is a", "item"]
    test_data = utils.list_to_dict(keys, values)
    expected_output = {"item": "hi", "item2": "this is a", "item3": "item"}
    second_test_data = utils.list_to_dict(keys[0:2], values)
    second_expected_output = {"item": "hi", "item2": "this is a", 2: "item"}
    third_test_data = utils.list_to_dict(keys, values[0:2])
    third_expected_output = {"item": "hi", "item2": "this is a", "item3": ""}
    assert test_data == expected_output
    assert second_test_data == second_expected_output
    assert third_test_data == third_expected_output


def test_camelcase_to_snakecase() -> None:
    camelcase_string = "thisIsATest"
    test_data = utils.camelcase_to_snakecase(camelcase_string)
    expected_output = "this_is_a_test"
    assert test_data == expected_output


def test_is_valid_format() -> None:
    date = "2019-03-30 00:00:00"
    invalid_date = "2019/03/30 00:00:00"
    assert datetime_utils.is_valid_format(date)
    assert not datetime_utils.is_valid_format(invalid_date)


@pytest.mark.changes_db
async def test_create_user() -> None:
    timezone = pytz.timezone(TIME_ZONE)

    async def get_user_attrs(
        email: str, attrs: List[str]
    ) -> Dict[str, Union[str, datetime]]:
        user_attrs = await users_domain.get_attributes(email, attrs)
        if "last_login" in user_attrs:
            user_attrs["last_login"] = timezone.localize(
                datetime.strptime(
                    user_attrs["last_login"], "%Y-%m-%d %H:%M:%S"
                )
            )
        return user_attrs

    now: datetime = datetime.now(tz=timezone)
    email: str = "integratescustomer@fluidattacks.com"
    user_info = await get_user_attrs(email, ["registered", "last_login"])
    assert user_info["registered"]
    assert user_info["last_login"] < now  # type: ignore

    time.sleep(1)
    await log_user_in({"email": email})
    user_info = await get_user_attrs(email, ["last_login"])
    assert user_info["last_login"] > now  # type: ignore
