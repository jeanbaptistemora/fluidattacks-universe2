# pylint: disable=import-error
from app.views.auth import (
    log_stakeholder_in,
)
from back.test.unit.src.utils import (
    create_dummy_session,
    create_dummy_simple_session,
)
from collections import (
    defaultdict,
)
from context import (
    FI_JWT_SECRET_API_RS512,
    FI_JWT_SECRET_RS512,
)
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
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
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
    StateSessionType,
)
from freezegun import (
    freeze_time,
)
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jws import (
    InvalidJWSSignature,
)
from jwcrypto.jwt import (
    JWT,
)
from newutils import (
    datetime as datetime_utils,
    files as files_utils,
    utils,
)
from organizations import (
    utils as orgs_utils,
)
import os
import pytest
import pytz
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from sessions.types import (
    UserAccessInfo,
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


def test_get_secret_session_token() -> None:
    user_email = "unittest"
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    secret = sessions_utils.get_secret(JWT(jwt=token))
    assert secret == FI_JWT_SECRET_RS512


def test_get_secret_api_token() -> None:
    user_email = "unittest"
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="api_token",
    )
    secret = sessions_utils.get_secret(JWT(jwt=token))
    assert secret == FI_JWT_SECRET_API_RS512


def test_decode_jwe() -> None:
    user_email = "unittest"
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": "e52615d33d77a21ba886d5a6d002a7b \
                b3e9b07c4b6e8e4aec87d96ca5161dd12",
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="api_token",
        api=True,
    )
    jwt_token = JWT(jwt=token)
    secret = sessions_utils.get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    jwt_token.validate(jws_key)
    decoded_payload = sessions_utils.decode_jwe(jwt_token.token.payload)
    assert decoded_payload == payload


def test_invalid_token_signature() -> None:
    user_email = "unittest"
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="api_token",
    )
    jwt_token = JWT(jwt=token)
    secret = sessions_utils.get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    with pytest.raises(InvalidJWSSignature):
        jwt_token.validate(jws_key)


async def test_get_jwt_content() -> None:
    request = create_dummy_simple_session()
    user_email = "unittest"
    jti = sessions_utils.calculate_hash_token()["jti"]
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": jti,
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    request.cookies[JWT_COOKIE_NAME] = token
    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=jti, state=StateSessionType.IS_VALID
            )
        ),
    )
    test_data = await sessions_domain.get_jwt_content(request)
    expected_output = {
        "user_email": user_email,
        "exp": expiration_time,
        "sub": "starlette_session",
        "jti": jti,
    }
    assert test_data == expected_output


async def test_valid_token() -> None:
    request = create_dummy_simple_session()
    user_email = "unittest"
    jti = sessions_utils.calculate_hash_token()["jti"]
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload={
            "user_email": user_email,
            "jti": jti,
        },
        subject="starlette_session",
    )
    request.cookies[JWT_COOKIE_NAME] = token
    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=jti, state=StateSessionType.IS_VALID
            )
        ),
    )
    test_data = await sessions_domain.get_jwt_content(request)
    expected_output = {
        "user_email": "unittest",
        "exp": expiration_time,
        "sub": "starlette_session",
        "jti": jti,
    }
    assert test_data == expected_output


async def test_valid_api_token() -> None:
    request = create_dummy_simple_session()
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": "unittest",
        "iat": int(datetime.utcnow().timestamp()),
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="api_token",
        api=True,
    )
    request.cookies[JWT_COOKIE_NAME] = token
    test_data = await sessions_domain.get_jwt_content(request)
    expected_output = {
        "user_email": "unittest",
        "exp": expiration_time,
        "iat": payload["iat"],
        "sub": "api_token",
        "jti": payload["jti"],
    }
    assert test_data == expected_output


@freeze_time("2022-10-19")
async def test_expired_token() -> None:
    request = create_dummy_simple_session()
    date = "2022-10-18 00:00:00"
    expiration_time = datetime_utils.get_as_epoch(
        datetime_utils.get_from_str(date)
    )
    payload = {
        "user_email": "unittest",
        "iat": int(datetime_utils.get_from_str(date).timestamp()),
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="api_token",
        api=True,
    )
    request.cookies[JWT_COOKIE_NAME] = token

    with pytest.raises(InvalidAuthorization):
        assert await sessions_domain.get_jwt_content(request)


async def test_token_expired() -> None:
    user_email = "integratesuser@gmail.com"
    request = await create_dummy_session(user_email)
    setattr(request, "store", defaultdict(lambda: None))
    assert await sessions_domain.get_jwt_content(request)

    new_request = await create_dummy_session(user_email)
    setattr(new_request, "store", defaultdict(lambda: None))
    assert await sessions_domain.get_jwt_content(new_request)

    with pytest.raises(ExpiredToken):
        setattr(request, "store", defaultdict(lambda: None))
        assert await sessions_domain.get_jwt_content(request)

    setattr(new_request, "store", defaultdict(lambda: None))
    assert await sessions_domain.get_jwt_content(new_request)


async def test_revoked_token() -> None:
    request = create_dummy_simple_session()
    user_email = "unittest"
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    payload = {
        "user_email": user_email,
        "jti": sessions_utils.calculate_hash_token()["jti"],
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    request.cookies[JWT_COOKIE_NAME] = token

    with pytest.raises(ExpiredToken):
        assert await sessions_domain.get_jwt_content(request)


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
    user_info = await loaders.stakeholder.load(email)
    assert user_info
    assert user_info.is_registered
    assert user_info.last_login_date
    assert user_info.last_login_date < now

    time.sleep(1)
    await log_stakeholder_in(
        loaders=loaders,
        user_info=UserAccessInfo(
            first_name="First_Name", last_name="Last_Name", user_email=email
        ),
    )
    new_loader: Dataloaders = get_new_context()
    new_user_info = await new_loader.stakeholder.load(email)
    assert new_user_info
    assert new_user_info.last_login_date
    assert new_user_info.last_login_date > now


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
