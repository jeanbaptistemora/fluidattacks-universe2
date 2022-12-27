from model.core_model import (
    FindingEnum,
)
from typing import (
    Dict,
    Set,
)
from utils.string import (
    complete_attrs_on_set,
)

BY_OBJ_NO_TYPE_ARGS_PROPAG: Dict[str, Set[str]] = {
    FindingEnum.F127.name: complete_attrs_on_set(
        {
            "Exec",
            "ExecContext",
            "Query",
            "QueryContext",
            "QueryRow",
            "QueryRowContext",
        }
    ),
}
