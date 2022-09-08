# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
import json
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    cast,
)


def safe_encode(string: str) -> str:
    """Turn a utf-8 string into a string of [a-z0-9] characters."""
    return string.encode("utf-8").hex().lower()


def safe_decode(hexstr: str) -> str:
    """Inverse of safe_encode."""
    return bytes.fromhex(hexstr).decode("utf-8")


def jwt_payload_encode(payload: dict[str, Any]) -> str:
    def hook(obj: object) -> str:
        # special cases where json encoder does not handle the object type
        # or a special format is needed
        if isinstance(obj, datetime):
            return datetime_utils.get_as_str(
                obj, date_format="%Y-%m-%dT%H:%M:%S.%f", zone="UTC"
            )
        # let JSONEncoder handle unsupported object types
        return cast(str, json.JSONEncoder().default(obj))

    encoder = json.JSONEncoder(default=hook)
    return encoder.encode(payload)


def jwt_payload_decode(payload: str) -> dict[str, Any]:
    def hook(jwt_payload: dict[str, Any]) -> dict[str, Any]:
        if "exp" in jwt_payload:
            exp = jwt_payload["exp"]
            if isinstance(exp, int):
                exp = datetime.fromtimestamp(exp)
            else:
                exp = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S.%f")
            jwt_payload["exp"] = exp
        return jwt_payload

    decoder = json.JSONDecoder(object_hook=hook)
    return cast(dict[str, Any], decoder.decode(payload))
