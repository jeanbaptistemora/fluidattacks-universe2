from ._decode import (
    decode,
)
from fa_purity import (
    Cmd,
    JsonObj,
    Result,
)
from fa_purity.json import (
    factory as JsonFactory,
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
from tap_mandrill.api.export._core import (
    ExportJob,
)

LOG = logging.getLogger(__name__)


def export_activity(client: Client) -> Cmd[ExportJob]:  # type: ignore[no-any-unimported]
    def _action() -> ExportJob:
        job: Result[JsonObj, ErrorAtInput] = (
            handle_api_error(
                lambda: client.exports.activity()  # type: ignore[misc, no-any-return]
            )
            .alt(lambda e: ErrorAtInput(e, ""))
            .bind(
                lambda r: JsonFactory.from_any(r).alt(lambda e: ErrorAtInput(e, str(r)))  # type: ignore[misc]
            )
        )
        export = (
            job.bind(
                lambda j: decode(j).alt(lambda e: ErrorAtInput(e, str(j)))
            )
            .alt(lambda e: e.raise_err(LOG))  # type: ignore[misc]
            .unwrap()
        )
        LOG.info("Peding export: %s", export)
        return export

    return Cmd.from_cmd(_action)
