from . import (
    _emit,
    _reports,
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
from fa_purity.date_time import (
    DatetimeUTC,
)
import logging
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
from tap_checkly.singer import (
    encoders,
)
from tap_checkly.state import (
    EtlState,
)

LOG = logging.getLogger(__name__)


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

    def check_reports_2(
        self, from_date: DatetimeUTC, to_date: DatetimeUTC
    ) -> Cmd[None]:
        client = CheckReportClient.new(self.creds)
        return _emit.from_encoder(
            encoders.bulk_reports,
            _reports.daily_reports(client, from_date, to_date),
        )

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
        msg1 = Cmd.from_cmd(
            lambda: LOG.info("check_results start date: %s", start_date)
        )
        msg2 = Cmd.from_cmd(
            lambda: LOG.info("check_results end date: %s", end_date)
        )
        client = ChecksClient.new(self.creds, 100)
        new_state = EtlState(
            Maybe.from_value(DateInterval.new(start_date, end_date).unwrap())
        )
        items = client.list_ids().bind(
            lambda c: client.list_check_results(c, start_date, end_date)
        )
        return (
            msg1
            + msg2
            + _emit.from_encoder(encoders.results, items)
            + _emit.emit_state(new_state)
        )


__all__ = [
    "decode_state",
    "SupportedStreams",
]
