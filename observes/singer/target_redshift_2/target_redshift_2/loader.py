# Standard libraries
from typing import (
    List,
    Tuple,
)
# Third party libraries
# Local libraries
from target_redshift_2.singer import (
    SingerObject,
    SingerRecord,
    SingerSchema,
)
from target_redshift_2.utils import Transform

ClassifiedSinger = Tuple[List[SingerSchema], List[SingerRecord]]


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
