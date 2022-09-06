# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from typing import (
    Any,
    Dict,
    NamedTuple,
)

# Payloads
DynamoDelete = NamedTuple("DynamoDelete", [("Key", Dict[str, Any])])
