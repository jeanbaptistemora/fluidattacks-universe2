# Standard libraries
from typing import (
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    List,
    NamedTuple,
    Set,
    Tuple,
)
# Third party libraries
# Local libraries
from postgres_client.cursor import CursorExeAction
from postgres_client.table import (
    IsolatedColumn,
    Table,
    TableID,
)
from singer_io.singer import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from target_redshift_2.objects import (
    RedshiftRecord,
    RedshiftSchema,
)
from target_redshift_2.utils import Transform

ClassifiedSinger = Tuple[List[SingerSchema], List[SingerRecord]]
TidRschemaMap = Dict[TableID, RedshiftSchema]
RRecordCreator = Callable[
    [Iterable[SingerRecord], TidRschemaMap], Iterable[RedshiftRecord]
]
TidTableMap = Dict[TableID, Table]


class Loader(NamedTuple):
    update_schema: Callable[[SingerSchema], None]
    upload_record: Callable[[SingerRecord, Set[SingerSchema]], None]
    upload_and_save_state: Callable[[SingerRecord, SingerState], None]


def process_lines_builder(
    deserialize: Transform[str, SingerMessage]
) -> Transform[List[str], ClassifiedSinger]:
    """Returns clasifier function of `SingerMessage`"""
    def process(lines: List[str]) -> ClassifiedSinger:
        """Separate `SingerSchema` and `SingerRecord` from lines"""
        s_schemas: List[SingerSchema] = []
        s_records: List[SingerRecord] = []
        singer_msg: SingerMessage
        for line in lines:
            singer_msg = deserialize(line)
            if isinstance(singer_msg, SingerSchema):
                s_schemas.append(singer_msg)
            elif isinstance(singer_msg, SingerRecord):
                s_records.append(singer_msg)
        return (s_schemas, s_records)

    return process


def create_table_schema_map_builder(
    to_rschema: Transform[SingerSchema, RedshiftSchema],
    extract_table_id: Transform[RedshiftSchema, TableID]
) -> Transform[Iterable[SingerSchema], TidRschemaMap]:
    """Returns creator of `TidRschemaMap`"""
    def table_map(s_schemas: Iterable[SingerSchema]) -> Dict[
        TableID, RedshiftSchema
    ]:
        """Returns `TidRschemaMap` from various `SingerSchema`"""
        mapper: TidRschemaMap = {}
        for s_schema in s_schemas:
            r_schema = to_rschema(s_schema)
            table_id = extract_table_id(r_schema)
            if table_id in mapper:
                prev_rschema: RedshiftSchema = mapper[table_id]
                mapper[table_id] = RedshiftSchema(
                    fields=prev_rschema.fields.union(r_schema.fields),
                    schema_name=r_schema.schema_name,
                    table_name=r_schema.table_name
                )
            else:
                mapper[table_id] = r_schema
        return mapper

    return table_map


def create_redshift_records_builder(
    to_rrecord: Callable[[SingerRecord, RedshiftSchema], RedshiftRecord],
    extract_table_id: Transform[SingerRecord, TableID]
) -> RRecordCreator:
    """Returns implemented `RRecordCreator`"""
    def create_rrecords(
        s_records: Iterable[SingerRecord], schema_map: TidRschemaMap
    ) -> Iterable[RedshiftRecord]:
        """Creates `RedshiftRecord`s from `SingerRecord`s and a rschema map"""
        r_records = []
        for s_record in s_records:
            table_id = extract_table_id(s_record)
            r_record = to_rrecord(s_record, schema_map[table_id])
            r_records.append(r_record)
        return r_records

    return create_rrecords


def create_table_mapper_builder(
    retrieve_table: Transform[TableID, Table]
) -> Transform[Iterable[TableID], TidTableMap]:
    """Returns implemented `TidTableMap`"""
    def create_table_mapper(table_ids: Iterable[TableID]) -> TidTableMap:
        """
        Retrieves real tables from table ids and return a map between them
        """
        mapper = {}
        for table_id in table_ids:
            table = retrieve_table(table_id)
            mapper[table_id] = table
        return mapper
    return create_table_mapper


def _update_schema(
    tables_map: TidTableMap,
    table_schema_map: TidRschemaMap,
    to_columns: Transform[RedshiftSchema, FrozenSet[IsolatedColumn]],
    add_columns: Callable[
        [Table, FrozenSet[IsolatedColumn]], List[CursorExeAction]
    ]
) -> None:
    def adjust_columns(
        items: Tuple[TableID, RedshiftSchema]
    ) -> List[CursorExeAction]:
        table_id = items[0]
        schema = items[1]
        table: Table = tables_map[table_id]
        return add_columns(table, to_columns(schema))

    actions = list(map(adjust_columns, table_schema_map.items()))
    for sub_actions in actions:
        for action in sub_actions:
            action.act()
