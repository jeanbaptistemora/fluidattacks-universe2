from __future__ import (
    annotations,
)

from .._core import (
    ExportJob,
)
from ._decode import (
    decode,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Result,
)
from fa_purity.json import (
    factory as JsonFactory,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
import logging
from mailchimp_transactional import (
    Client,
)
from tap_mandrill._utils import (
    ErrorAtInput,
)
from tap_mandrill.api._utils import (
    handle_api_error,
)

LOG = logging.getLogger(__name__)


def get_jobs(client: Client) -> Cmd[FrozenList[ExportJob]]:  # type: ignore[no-any-unimported]
    def _action() -> FrozenList[ExportJob]:
        jobs: Result[FrozenList[JsonObj], ErrorAtInput] = (
            handle_api_error(
                lambda: client.exports.list()  # type: ignore[misc, no-any-return]
            )
            .alt(lambda e: ErrorAtInput(Exception(e), ""))
            .bind(
                lambda r: JsonFactory.json_list(r).alt(lambda e: ErrorAtInput(e, str(r)))  # type: ignore[misc]
            )
        )
        return (
            jobs.bind(
                lambda l: all_ok(
                    pure_map(
                        lambda i: decode(i).alt(
                            lambda e: ErrorAtInput(e, str(i))
                        ),
                        l,
                    ).transform(lambda x: tuple(x))
                )
            )
            .alt(lambda e: e.raise_err(LOG))  # type: ignore[misc]
            .unwrap()
        )

    return Cmd.from_cmd(_action)
