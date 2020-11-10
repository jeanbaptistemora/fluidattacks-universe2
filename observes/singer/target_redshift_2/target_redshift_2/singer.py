# Standard libraries
import json
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    List,
    NamedTuple,
    Optional,
    Union,
)
# Third party libraries
# Local libraries


class SingerSchema(NamedTuple):
    stream: str
    schema: Dict[str, Any]
    key_properties: FrozenSet[str]
    bookmark_properties: Optional[FrozenSet[str]] = None


class SingerSchemaFactory(NamedTuple):
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    load_json: Callable[[str], Any] = json.loads

    def deserialize(
        self: 'SingerSchemaFactory',
        json_schema: str
    ) -> SingerSchema:
        try:
            raw_json: Dict[str, Any] = self.load_json(json_schema)
            if raw_json['type'] == 'SCHEMA':
                bookmark_properties: Optional[List[str]] = raw_json.get(
                    'bookmark_properties', None
                )
                return SingerSchema(
                    raw_json['stream'],
                    raw_json['schema'],
                    frozenset(raw_json['key_properties']),
                    frozenset(bookmark_properties)
                    if bookmark_properties else None,
                )
            raise KeyError()
        except KeyError:
            raise KeyError('Deserialize singer schema failed. Missing fields.')


class SingerRecord(NamedTuple):
    stream: str
    record: Dict[str, Any]
    time_extracted: Optional[str] = None


class SingerRecordFactory(NamedTuple):
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    load_json: Callable[[str], Any] = json.loads

    def deserialize(
        self: 'SingerRecordFactory',
        json_record: str
    ) -> SingerRecord:
        try:
            raw_json = self.load_json(json_record)
            if raw_json['type'] == 'RECORD':
                return SingerRecord(
                    raw_json['stream'],
                    raw_json['record'],
                    raw_json.get('time_extracted', None)
                )
            raise KeyError()
        except KeyError:
            raise KeyError('Deserialize singer schema failed. Missing fields.')


class SingerFactory(NamedTuple):
    # pylint: disable=too-many-function-args
    # required due to a bug with callable properties
    load_json: Callable[[str], Any] = json.loads
    record_factory: SingerRecordFactory = SingerRecordFactory()
    schema_factory: SingerSchemaFactory = SingerSchemaFactory()

    def deserialize(
        self: 'SingerFactory',
        json_record: str
    ) -> Union[SingerRecord, SingerSchema]:
        raw_json: Dict[str, Any] = self.load_json(json_record)
        data_type: Optional[str] = raw_json.get('type', None)
        if data_type == 'RECORD':
            return self.record_factory.deserialize(json_record)
        if data_type == 'SCHEMA':
            return self.schema_factory.deserialize(json_record)
        raise KeyError(
            f'Deserialize singer failed. Unknown or missing type {data_type}.'
        )
