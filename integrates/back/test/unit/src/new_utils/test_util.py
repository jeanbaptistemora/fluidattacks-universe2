# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=protected-access, import-error
from app.views.auth import (
    log_stakeholder_in,
)
from app.views.types import (
    UserAccessInfo,
)
from back.test.unit.src.utils import (
    create_dummy_session,
    create_dummy_simple_session,
)
from collections import (
    defaultdict,
)
from custom_exceptions import (
    ExpiredToken,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
    StateSessionType,
)
from jwcrypto.jwe import (
    InvalidJWEData,
    JWException,
)
from newutils import (
    datetime as datetime_utils,
    encodings,
    files as files_utils,
    token as token_utils,
    utils,
)
from organizations import (
    utils as orgs_utils,
)
import os
import pytest
import pytz
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


async def test_payload_encrypt_decrypt_always_check() -> None:
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }

    result = token_utils._decrypt_jwt_payload(
        token_utils._encrypt_jwt_payload(payload),
    )
    assert payload == result

    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "iat": datetime.utcnow().timestamp(),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    with pytest.raises(JWException):
        token_utils._decrypt_jwt_payload(payload)


async def test_decrypt_temp_support_for_nonencrypted() -> None:
    payload = {
        "user_email": "unittest",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "iat": datetime.utcnow().timestamp(),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    with pytest.raises(InvalidJWEData):
        token_utils._decrypt_jwt_payload(payload)


async def test_get_jwt_content() -> None:
    request = create_dummy_simple_session()
    user_email = "unittest"
    jti = token_utils.calculate_hash_token()["jti"]
    payload = {
        "user_email": user_email,
        "exp": datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        ),
        "sub": "starlette_session",
        "jti": jti,
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=jti, state=StateSessionType.IS_VALID
            )
        ),
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],  # type: ignore
        value=payload["jti"],
        ttl=SESSION_COOKIE_AGE,
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],  # type: ignore
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
        "exp": datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        ),
        "sub": "session_token",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(
        f'fi_jwt:{payload["jti"]}', token, SESSION_COOKIE_AGE  # type: ignore
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],  # type: ignore
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
        "exp": datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        ),
        "iat": int(datetime.utcnow().timestamp()),
        "sub": "api_token",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload, api=True)
    request.cookies[JWT_COOKIE_NAME] = token
    await sessions_dal.add_element(
        f'fi_jwt:{payload["jti"]}', token, SESSION_COOKIE_AGE  # type: ignore
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=payload["user_email"],  # type: ignore
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
        "exp": datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        ),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],  # type: ignore
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
        "exp": datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        ),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    request.cookies[JWT_COOKIE_NAME] = token
    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],  # type: ignore
        value=payload["jti"],
        ttl=SESSION_COOKIE_AGE,
    )
    await redis_del_entity_attr(
        entity="session",
        attr="jti",
        email=payload["user_email"],  # type: ignore
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
    test_data = utils.list_to_dict(keys, values)  # type: ignore
    expected_output = {"item": "hi", "item2": "this is a", "item3": "item"}
    second_test_data = utils.list_to_dict(keys[0:2], values)  # type: ignore
    second_expected_output = {"item": "hi", "item2": "this is a", 2: "item"}
    third_test_data = utils.list_to_dict(keys, values[0:2])  # type: ignore
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
    loaders: Dataloaders = get_new_context()

    now: datetime = datetime.now(tz=timezone)
    email: str = "integratesuser2@fluidattacks.com"
    user_info: Stakeholder = await loaders.stakeholder.load(email)
    assert user_info.is_registered
    assert (
        datetime_utils.get_datetime_from_iso_str(
            user_info.last_login_date  # type: ignore
        )
        < now
    )

    time.sleep(1)
    await log_stakeholder_in(
        loaders=loaders,
        stakeholder=UserAccessInfo(
            first_name="First_Name", last_name="Last_Name", user_email=email
        ),
    )
    new_loader: Dataloaders = get_new_context()
    new_user_info: Stakeholder = await new_loader.stakeholder.load(email)
    user_last_login_date = datetime_utils.get_datetime_from_iso_str(
        new_user_info.last_login_date  # type: ignore
    )
    assert user_last_login_date > now


def test_format_credential_key() -> None:
    key_1 = "VGVzdCBTU0g="
    expected_key_1 = "VGVzdCBTU0gK"
    assert (
        orgs_utils.format_credentials_ssh_key(ssh_key=key_1) == expected_key_1
    )
    assert (
        orgs_utils.format_credentials_ssh_key(ssh_key=expected_key_1)
        == expected_key_1
    )
