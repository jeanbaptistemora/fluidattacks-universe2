from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_singer_io.singer import (
    SingerMessage,
)
from redshift_client.id_objs import (
    SchemaId,
)
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
class OutputEmitter:
    _data: Stream[SingerMessage]
    loader: SingerLoader
    strategy: LoadingStrategy
    records_limit: int

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
