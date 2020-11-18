# Standard libraries
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Tuple,
)
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import SchemaID, TableID
from target_redshift_2.objects import RedshiftRecord, RedshiftSchema
from target_redshift_2.singer import (
    SingerObject,
    SingerRecord,
    SingerSchema,
)
from target_redshift_2.utils import Transform

ClassifiedSinger = Tuple[List[SingerSchema], List[SingerRecord]]
TableRschemaMap = Dict[TableID, RedshiftSchema]
RRecordCreator = Callable[
    [Iterable[SingerRecord], TableRschemaMap], Iterable[RedshiftRecord]
]


def process_lines_builder(
    deserialize: Transform[str, SingerObject]
) -> Transform[List[str], ClassifiedSinger]:
    """Returns clasifier function of `SingerObject`"""
    def process(lines: List[str]) -> ClassifiedSinger:
        """Separate `SingerSchema` and `SingerRecord` from lines"""
        s_schemas: List[SingerSchema] = []
        s_records: List[SingerRecord] = []
        singer_msg: SingerObject
        for line in lines:
            singer_msg = deserialize(line)
            if isinstance(singer_msg, SingerSchema):
                s_schemas.append(singer_msg)
            elif isinstance(singer_msg, SingerRecord):
                s_records.append(singer_msg)
        return (s_schemas, s_records)

    return process


def create_table_schema_map_builder(
    to_rschema: Transform[SingerSchema, RedshiftSchema]
) -> Transform[Iterable[SingerSchema], TableRschemaMap]:
    """Returns creator of `TableRschemaMap`"""
    def table_map(s_schemas: Iterable[SingerSchema]) -> Dict[
        TableID, RedshiftSchema
    ]:
        """Returns `TableRschemaMap` from various `SingerSchema`"""
        mapper = {}
        for s_schema in s_schemas:
            r_schema = to_rschema(s_schema)
            table_id = TableID(
                schema=SchemaID(None, schema_name=r_schema.schema_name),
                table_name=r_schema.table_name
            )
            mapper[table_id] = r_schema
        return mapper

    return table_map


def create_redshift_records_builder(
    to_rrecord: Callable[[SingerRecord, RedshiftSchema], RedshiftRecord],
    extract_table_id: Transform[SingerRecord, TableID]
) -> RRecordCreator:
    """Returns implemented `RRecordCreator`"""
    def create_rrecords(
        s_records: Iterable[SingerRecord], schema_map: TableRschemaMap
    ) -> Iterable[RedshiftRecord]:
        """Creates `RedshiftRecord`s from `SingerRecord`s and a rschema map"""
        r_records = []
        for s_record in s_records:
            table_id = extract_table_id(s_record)
            r_record = to_rrecord(s_record, schema_map[table_id])
            r_records.append(r_record)
        return r_records

    return create_rrecords
