# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Result,
)
from fa_purity.json.factory import (
    from_any,
    json_list,
)
from fa_purity.json.transform import (
    to_raw,
)
from fa_purity.union import (
    UnionFactory,
)
import logging
import requests
from requests.exceptions import (
    HTTPError,
    JSONDecodeError,
)

LOG = logging.getLogger(__name__)


class UnexpectedServerResponse(Exception):
    pass


@dataclass(frozen=True)
class HttpClient:
    _api_url: str

    def _full_endpoint(self, endpoint: str) -> str:
        return self._api_url + endpoint

    def get(
        self, endpoint: str, headers: JsonObj, params: JsonObj
    ) -> Cmd[
        Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]
    ]:
        def _action() -> Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]:
            target = self._full_endpoint(endpoint)
            LOG.info("API call (get): %s\nparams = %s", target, params)
            response = requests.get(
                target,
                headers=to_raw(headers),  # type: ignore[misc]
                params=to_raw(params),  # type: ignore[misc]
            )
            _union: UnionFactory[JsonObj, FrozenList[JsonObj]] = UnionFactory()
            try:
                response.raise_for_status()
                raw = response.json()  # type: ignore[misc]
                result = json_list(raw).map(_union.inr).lash(lambda _: from_any(raw).map(_union.inl))  # type: ignore[misc]
                result.alt(lambda e: ValueError()).unwrap()
                return result.alt(
                    lambda e: UnexpectedServerResponse(f"error: {str(e)}; raw response: {str(raw)}")  # type: ignore[misc]
                )
            except HTTPError as err:  # type: ignore[misc]
                return Result.failure(err)
            except JSONDecodeError as err:  # type: ignore[misc]
                return Result.failure(
                    UnexpectedServerResponse(f"JSONDecodeError: {err}")
                )

        return Cmd.from_cmd(_action)

    def post(
        self, endpoint: str, headers: JsonObj
    ) -> Cmd[Result[None, HTTPError]]:
        def _action() -> Result[None, HTTPError]:
            target = self._full_endpoint(endpoint)
            LOG.info("API call: %s\nmethod=%s", target, "post")
            response = requests.post(
                target,
                headers=to_raw(headers),  # type: ignore[misc]
            )
            try:
                response.raise_for_status()
            except HTTPError as err:  # type: ignore[misc]
                return Result.failure(err)
            return Result.success(None)

        return Cmd.from_cmd(_action)
