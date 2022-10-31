# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
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
from redshift_client.id_objs import (
    SchemaId,
)
import sys
from target_redshift import (
    grouper,
)
from target_redshift.loader import (
    SingerLoader,
)
from target_redshift.strategy import (
    LoadingStrategy,
)


@dataclass(frozen=True)
class Emitter:
    loader: SingerLoader
    strategy: LoadingStrategy
    records_limit: int

    @property
    def _data(self) -> Stream[SingerMessage]:
        cmd = Cmd.from_cmd(
            lambda: TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        )
        return unsafe_from_cmd(cmd.map(from_file).map(lambda x: iter(x)))

    def load_procedure(self, schema: SchemaId) -> Cmd[None]:
        return (
            self._data.transform(
                lambda d: grouper.group_records(d, self.records_limit)
            )
            .map(lambda p: self.loader.handle(schema, p))
            .transform(consume)
        )

    def main(self) -> Cmd[None]:
        return self.strategy.main(self.load_procedure)
