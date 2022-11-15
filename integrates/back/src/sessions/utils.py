# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_JWT_ENCRYPTION_KEY,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)
from custom_exceptions import (
    ExpiredToken,
)
from datetime import (
    datetime,
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
from typing import (
    Any,
    Dict,
)


def decode_jwe(payload: str) -> Dict[str, Any]:
    """Decodes a jwe token and returns its decrypted payload"""
    jwe_key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    jwe_token = JWE()
    jwe_token.deserialize(payload)
    jwe_token.decrypt(jwe_key)
    decoded_payload = json.loads(jwe_token.payload.decode("utf-8"))

    return decoded_payload


def get_secret(jwt_token: JWT) -> str:
    """Returns the secret needed to decrypt JWE"""
    # pylint: disable=protected-access
    payload = jwt_token._token.objects["payload"]
    deserialized_payload = json.loads(payload.decode("utf-8"))
    sub = deserialized_payload.get("sub")

    if sub is None:
        sub = decode_jwe(payload).get("sub")

    if sub == "api_token":
        return FI_JWT_SECRET_API
    return FI_JWT_SECRET


def validate_expiration_time(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "exp" not in payload:
        return payload

    exp = payload["exp"]
    utc_now = int(datetime.now().timestamp())
    if isinstance(exp, str):
        exp_as_datetime = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S.%f")
        exp = int(exp_as_datetime.timestamp())
        payload["exp"] = exp

    if exp < utc_now:
        raise ExpiredToken()

    return payload
