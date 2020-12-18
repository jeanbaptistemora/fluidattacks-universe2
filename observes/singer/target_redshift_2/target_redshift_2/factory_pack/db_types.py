# Standard libraries
from typing import (
    Any,
    Dict, FrozenSet,
    Optional,
)
# Third party libraries
# Local libraries
from postgres_client.table import DbTypes
from target_redshift_2.objects import AmbiguousType


JSON_SCHEMA_TYPES: Dict[DbTypes, Any] = {
    DbTypes.BOOLEAN: [
        {"type": "boolean"},
        {"type": ["boolean", "null"]},
        {"type": ["null", "boolean"]}
    ],
    DbTypes.NUMERIC: [
        {"type": "integer"},
        {"type": ["integer", "null"]},
        {"type": ["null", "integer"]}
    ],
    DbTypes.FLOAT: [
        {"type": "number"},
        {"type": ["number", "null"]},
        {"type": ["null", "number"]}
    ],
    DbTypes.VARCHAR: [
        {"type": "string"},
        {"type": ["string", "null"]},
        {"type": ["null", "string"]}
    ],
    DbTypes.TIMESTAMP: [
        {"type": "string", "format": "date-time"},
        {
            "anyOf": [
                {"type": "string", "format": "date-time"},
                {"type": ["string", "null"]},
            ]
        },
        {
            "anyOf": [
                {"type": "string", "format": "date-time"},
                {"type": ["null", "string"]},
            ]
        }
    ]
}


def from_dict(field_type: Dict[str, Any]) -> Optional[DbTypes]:
    matched_types: FrozenSet[DbTypes] = frozenset(
        map(
            lambda x: x[0],
            filter(
                lambda x: field_type in x[1],
                JSON_SCHEMA_TYPES.items()
            )
        )
    )
    if len(matched_types) > 1:
        raise AmbiguousType(f'Could not map {field_type} into a uniqe DbType')
    return next(iter(matched_types)) if matched_types else None
