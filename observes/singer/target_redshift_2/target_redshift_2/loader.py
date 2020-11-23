# Standard libraries
from typing import (
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    List, NamedTuple, Set,
    Tuple,
)
# Third party libraries
# Local libraries
from postgres_client.objects import (
    CursorExeAction,
    IsolatedColumn,
    Table,
    TableID,
)
from target_redshift_2.objects import (
    RedshiftRecord,
    RedshiftSchema,
)
from target_redshift_2.singer import (
    SingerObject,
    SingerRecord,
    SingerSchema,
)
from target_redshift_2.utils import Transform

ClassifiedSinger = Tuple[List[SingerSchema], List[SingerRecord]]
TidRschemaMap = Dict[TableID, RedshiftSchema]
RRecordCreator = Callable[
    [Iterable[SingerRecord], TidRschemaMap], Iterable[RedshiftRecord]
]
TidTableMap = Dict[TableID, Table]


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
    def create_table_mapper(table_ids: Iterable[TableID]):
        """
        Retrieves real tables from table ids and return a map between them
        """
        mapper = {}
        for table_id in table_ids:
            table = retrieve_table(table_id)
            mapper[table_id] = table
        return mapper
    return create_table_mapper


def update_schema_builder(
    to_columns: Transform[RedshiftSchema, FrozenSet[IsolatedColumn]],
    add_columns: Callable[
        [Table, FrozenSet[IsolatedColumn]], List[CursorExeAction]
    ]
) -> Callable[[TidTableMap, TidRschemaMap], None]:
    def update_schema(tables_map, table_schema_map):
        for table_id, schema in table_schema_map.items():
            table: Table = tables_map[table_id]
            actions = add_columns(table, to_columns(schema))
            for action in actions:
                action.act()
    return update_schema


class Loader(NamedTuple):
    process_lines: Transform[Iterable[str], ClassifiedSinger]
    create_table_schema_map: Transform[Iterable[SingerSchema], TidRschemaMap]
    create_rrecords: RRecordCreator
    create_table_mapper: Transform[Iterable[TableID], TidTableMap]
    update_schema: Callable[[TidTableMap, TidRschemaMap], None]
    upload_records: Callable[[Set[RedshiftRecord], TidTableMap], None]


def upload_lines(lines: List[str], loader: Loader):
    separated_singers: ClassifiedSinger = loader.process_lines(lines)
    tableid_schema_map: Dict[TableID, RedshiftSchema] = \
        loader.create_table_schema_map(separated_singers[0])
    rrecords: Iterable[RedshiftRecord] = loader.create_rrecords(
        separated_singers[1], tableid_schema_map
    )
    tables_map: TidTableMap = loader.create_table_mapper(
        set(tableid_schema_map.keys())
    )
    loader.update_schema(tables_map, tableid_schema_map)
    loader.upload_records(set(rrecords), tables_map)
