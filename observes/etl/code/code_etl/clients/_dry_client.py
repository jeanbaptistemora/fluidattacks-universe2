from ._real_client import (
    RealClient,
)
from code_etl.client import (
    Client,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)


@dataclass(frozen=True)
class DryRunClient:
    _real_client: RealClient

    def client(self) -> Client:
        do_nothing = Cmd.from_cmd(lambda: None)
        return Client.new(
            lambda _: do_nothing,
            self._real_client.all_data_count,
            self._real_client.get_context,
            lambda _: do_nothing,
            lambda _: do_nothing,
            self._real_client.namespace_data,
            lambda _: do_nothing,
        )
