# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._grouper import (
    group_records,
)
from ._handlers import (
    MutableTableMap,
    SingerHandler,
    SingerHandlerOptions,
)
from ._s3_loader import (
    S3Handler,
)
from ._strategy import (
    LoadingStrategy,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerSchema,
)
from fa_singer_io.singer.deserializer import (
    from_file,
)
from io import (
    TextIOWrapper,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.table.client import (
    TableClient,
)
import sys


def _stdin_buffer() -> Cmd[TextIOWrapper]:
    return Cmd.from_cmd(
        lambda: TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    )


def main(
    schema: SchemaId,
    client: TableClient,
    limit: int,
    options: SingerHandlerOptions,
) -> Cmd[None]:
    data: Stream[SingerMessage] = unsafe_from_cmd(
        _stdin_buffer().map(from_file).map(lambda x: iter(x))
    )
    handler = SingerHandler(schema, client, options)
    schemas = MutableTableMap({})
    cmds = data.transform(lambda d: group_records(d, limit)).map(
        lambda p: handler.handle(schemas, p)
    )
    return consume(cmds)


def from_s3(
    schema: SchemaId, client: TableClient, s3_handler: S3Handler
) -> Cmd[None]:
    data: Stream[SingerMessage] = unsafe_from_cmd(
        _stdin_buffer().map(from_file).map(lambda x: iter(x))
    )
    mock_options = SingerHandlerOptions(True, 1, 1)
    handler = SingerHandler(schema, client, mock_options)
    nothing = Cmd.from_cmd(lambda: None)
    return data.map(
        lambda s: handler.create_table(s) + s3_handler.handle_schema(s)
        if isinstance(s, SingerSchema)
        else nothing
    ).transform(consume)


__all__ = [
    "SingerHandlerOptions",
    "S3Handler",
    "LoadingStrategy",
]
