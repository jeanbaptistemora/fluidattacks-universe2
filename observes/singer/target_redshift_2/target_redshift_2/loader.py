# Standard libraries
from typing import (
    Dict,
    Iterable,
    List,
    Tuple,
)
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import SchemaID, TableID
from target_redshift_2.objects import RedshiftSchema
from target_redshift_2.singer import (
    SingerObject,
    SingerRecord,
    SingerSchema,
)
from target_redshift_2.utils import Transform

ClassifiedSinger = Tuple[List[SingerSchema], List[SingerRecord]]
TableRschemaMap = Dict[TableID, RedshiftSchema]


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
    def table_map(s_schemas: Iterable[SingerSchema]) -> Dict[
        TableID, RedshiftSchema
    ]:
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
