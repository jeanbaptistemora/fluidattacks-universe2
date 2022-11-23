import binascii
from context import (
    CI_COMMIT_REF_NAME,
    JWT_ENCRYPTION_KEY,
    JWT_SECRET,
    TEST_E2E_USER_1,
)
from datetime import (
    datetime,
    timedelta,
)
import json
from jwcrypto.jwe import (
    JWE,
)
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jwt import (
    JWT,
)
import secrets


def _get_jti() -> str:
    jti_token = secrets.token_bytes(32)
    return binascii.hexlify(jti_token).decode()


def _get_token() -> str:
    expiration_time = int(
        (datetime.utcnow() + timedelta(minutes=30)).timestamp()
    )
    jws_key = JWK.from_json(JWT_SECRET)
    jwe_key = JWK.from_json(JWT_ENCRYPTION_KEY)
    default_claims = {"exp": expiration_time, "sub": "test_e2e_session"}
    payload = {
        "user_email": TEST_E2E_USER_1,
        "first_name": "Test",
        "last_name": "Session",
        "jti": _get_jti(),
    }
    jwt_object = JWT(
        default_claims=default_claims,
        claims=JWE(
            algs=["A256GCM", "A256GCMKW"],
            plaintext=json.dumps(payload).encode("utf-8"),
            protected={
                "alg": "A256GCMKW",
                "enc": "A256GCM",
            },
            recipient=jwe_key,
        ).serialize(),
        header={"alg": "HS512"},
    )
    jwt_object.make_signed_token(jws_key)
    return jwt_object.serialize()


def append_session(test_content: str) -> str:
    instruction = f"""
    open URL "https://{CI_COMMIT_REF_NAME}.app.fluidattacks.com/"
    execute JavaScript in the browser text starting from next line and ending with [END]
        document.cookie = "integrates_session={_get_token()}"
    [END]
    """
    return "\n".join([instruction, test_content])
