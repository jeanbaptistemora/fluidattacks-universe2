# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _emit,
)
from ._objs import (
    SupportedStreams,
)
from ._state import (
    decode as decode_state,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.stream.transform import (
    chain,
)
from tap_checkly._utils import (
    DateInterval,
)
from tap_checkly.api import (
    Credentials,
)
from tap_checkly.api.alert_channels import (
    AlertChannelsClient,
)
from tap_checkly.api.checks import (
    ChecksClient,
)
from tap_checkly.api.checks.status import (
    CheckStatusClient,
)
from tap_checkly.api.groups import (
    CheckGroupClient,
)
from tap_checkly.api.report import (
    CheckReportClient,
)
from tap_checkly.objs import (
    IndexedObj,
)
from tap_checkly.singer import (
    encoders,
)
from tap_checkly.singer._checks.results.records import (
    encode_result,
)
from tap_checkly.state import (
    EtlState,
)


@dataclass(frozen=True)
class Streams:
    creds: Credentials
    old_date: datetime
    now: datetime

    def alert_chs(self) -> Cmd[None]:
        client = AlertChannelsClient.new(self.creds, 100)
        return _emit.from_encoder(encoders.alerts, client.list_all())

    def all_checks(self) -> Cmd[None]:
        client = ChecksClient.new(self.creds, 100)
        return _emit.from_encoder(encoders.checks, client.list_checks())

    def check_reports(self) -> Cmd[None]:
        client = CheckReportClient.new(self.creds)
        return _emit.from_encoder(encoders.report, client.reports_stream())

    def check_groups(self) -> Cmd[None]:
        client = CheckGroupClient.new(self.creds, 100)
        return _emit.from_encoder(encoders.groups, client.list_all())

    def check_status(self) -> Cmd[None]:
        client = CheckStatusClient.new(self.creds, 100)
        return _emit.from_encoder(encoders.status, client.list_all())

    def check_results(self, state: EtlState) -> Cmd[None]:
        start_date = state.results.map(lambda d: d.newest).value_or(
            self.old_date
        )
        end_date = self.now
        client = ChecksClient.new(self.creds, 100)
        new_state = EtlState(
            Maybe.from_value(DateInterval.new(start_date, end_date).unwrap())
        )
        return _emit.emit_stream(
            client.list_ids()
            .bind(lambda c: client.list_check_results(c, start_date, end_date))
            .map(encode_result)
            .transform(chain),
        ) + _emit.emit_state(new_state)


__all__ = [
    "decode_state",
    "SupportedStreams",
]
