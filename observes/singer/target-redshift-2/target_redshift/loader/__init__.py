from ._common import (
    SingerHandler,
    SingerHandlerOptions,
)
from ._core import (
    SingerLoader,
)
from ._s3_loader import (
    S3Handler,
)
from fa_purity import (
    Cmd,
    Maybe,
    Stream,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerSchema,
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
from target_redshift.loader._handlers import (
    StateKeeperS3,
)
from target_redshift.loader._loaders import (
    Loaders,
)


def from_s3(
    data: Stream[SingerMessage],
    schema: SchemaId,
    client: TableClient,
    s3_handler: S3Handler,
) -> Cmd[None]:
    mock_options = SingerHandlerOptions(True, 1, 1)
    handler = SingerHandler(schema, client, mock_options, Maybe.empty())
    nothing = Cmd.from_cmd(lambda: None)
    return data.map(
        lambda s: handler.schema_handler(s) + s3_handler.handle_schema(s)
        if isinstance(s, SingerSchema)
        else nothing
    ).transform(consume)


__all__ = [
    "SingerLoader",
    "SingerHandlerOptions",
    "S3Handler",
    "Loaders",
    "StateKeeperS3",
]
