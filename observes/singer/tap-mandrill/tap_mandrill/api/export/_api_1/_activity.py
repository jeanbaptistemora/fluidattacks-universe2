from .._api_key import (
    ApiKey,
    KeyAccess,
)
from .._core import (
    ApiPath,
    EPOCH,
    NOW,
)
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
import requests
from tap_mandrill._utils import (
    ErrorAtInput,
)
from tap_mandrill.api._utils import (
    handle_api_error,
)
from tap_mandrill.api.export._core import (
    ExportJob,
)
from typing import (
    Dict,
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


def export_activity_2(api_key: ApiKey) -> Cmd[ExportJob]:
    path = ApiPath.from_raw("exports", "activity")
    args: Dict[str, str] = {
        "key": api_key.extract(KeyAccess()),
        "date_from": EPOCH.strftime("%Y-%m-%d %H:%M:%S"),
        "date_to": NOW.strftime("%Y-%m-%d %H:%M:%S"),
    }

    def _action() -> ExportJob:
        response = requests.post(path.full_url, json=args)
        job: Result[JsonObj, ErrorAtInput] = JsonFactory.from_any(
            response.json()  # type: ignore[misc]
        ).alt(
            lambda e: ErrorAtInput(e, str(response.json()))  # type: ignore[misc]
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
