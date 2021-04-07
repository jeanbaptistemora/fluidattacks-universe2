# Standard libraries
import functools
from typing import (
    Any,
    Dict,
    List,
)
# Third party libraries
# Local libraries
from target_redshift_2.factory_pack import db_types


def test_db_type() -> None:
    # Arrange
    dict_types: List[Dict[str, Any]] = functools.reduce(
        lambda a, b: a + b,
        db_types.JSON_SCHEMA_TYPES.values()
    )
    for dtype in dict_types:
        # Act
        result = db_types.from_dict(dtype)
        # Assert
        assert result is not None
        assert dtype in db_types.JSON_SCHEMA_TYPES[result]
