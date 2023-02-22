from purity.v2.json.factory import (
    JsonObj,
)
from purity.v2.json.value import (
    transform as jval_transform,
)
from typing import (
    Any,
    Dict,
)


def to_raw(json_obj: JsonObj) -> Dict[str, Any]:
    return {key: jval_transform.to_raw(val) for key, val in json_obj.items()}
