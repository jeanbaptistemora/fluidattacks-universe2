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
)
from fa_singer_io.singer.deserializer import (
    from_file,
)
from io import (
    TextIOWrapper,
)
import sys
from target_snowflake.snowflake_client.schema import (
    SchemaManager,
)


def _stdin_buffer() -> Cmd[TextIOWrapper]:
    return Cmd.from_cmd(
        lambda: TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    )


def main(
    manager: SchemaManager,
    limit: int,
    options: SingerHandlerOptions,
) -> Cmd[None]:
    data: Stream[SingerMessage] = unsafe_from_cmd(
        _stdin_buffer().map(from_file).map(lambda x: iter(x))
    )
    handler = SingerHandler(manager, options)
    schemas = MutableTableMap({})
    cmds = data.transform(lambda d: group_records(d, limit)).map(
        lambda p: handler.handle(schemas, p)
    )
    return consume(cmds)


__all__ = [
    "SingerHandlerOptions",
    "LoadingStrategy",
]
