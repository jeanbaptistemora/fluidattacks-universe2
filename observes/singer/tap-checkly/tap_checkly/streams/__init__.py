# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _emitter,
)
from ._objs import (
    SupportedStreams,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.pure_iter import (
    transform as PIterTransform,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
from paginator import (
    AllPages,
)
from returns.io import (
    IO,
)
import sys
from tap_checkly.api2 import (
    Credentials,
)
from tap_checkly.api2.alert_channels import (
    AlertChannelsClient,
)
from tap_checkly.api2.checks import (
    ChecksClient,
)
from tap_checkly.api2.checks.status import (
    CheckStatusClient,
)
from tap_checkly.api2.groups import (
    CheckGroupClient,
)
from tap_checkly.api2.report import (
    CheckReportClient,
)
from tap_checkly.api import (
    ApiClient,
    ApiPage,
)
from tap_checkly.objs import (
    IndexedObj,
)
from tap_checkly.singer import (
    encoders,
    ObjEncoder,
)
from tap_checkly.singer._checks.results.records import (
    encode_result,
)
from typing import (
    Iterator,
    TypeVar,
)

ALL = AllPages()


def _emit_stream(
    records: Stream[SingerRecord],
) -> Cmd[None]:
    emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
    return consume(emissions)


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[IO[ApiPage]],
) -> Cmd[None]:
    def action() -> None:
        for page in pages:
            _emitter.emit_iopage(stream, page)

    return Cmd.from_cmd(action)


def all_dashboards(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.DASHBOARD,
        api.dashboards.list_dashboards(ALL),
    )


def all_env_vars(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.ENV_VARS,
        api.env.list_env_vars(ALL),
    )


def all_maint_windows(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.MAINTENACE_WINDOWS,
        api.maintenance.list_mant_windows(ALL),
    )


def all_snippets(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.SNIPPETS,
        api.snippets.list_snippets(ALL),
    )


_T = TypeVar("_T")


@dataclass(frozen=True)
class Streams:
    creds: Credentials
    old_date: datetime
    now: datetime

    @staticmethod
    def _from_encoder(encoder: ObjEncoder[_T], items: Stream[_T]) -> Cmd[None]:
        schemas = encoder.schemas.map(
            lambda s: emitter.emit(sys.stdout, s)
        ).transform(PIterTransform.consume)
        return schemas + _emit_stream(
            items.map(encoder.record).transform(chain)
        )

    def alert_chs(self) -> Cmd[None]:
        client = AlertChannelsClient.new(self.creds, 100)
        return self._from_encoder(encoders.alerts, client.list_all())

    def all_checks(self) -> Cmd[None]:
        client = ChecksClient.new(self.creds, 100, self.old_date, self.now)
        return self._from_encoder(encoders.checks, client.list_checks())

    def check_reports(self) -> Cmd[None]:
        client = CheckReportClient.new(self.creds)
        return self._from_encoder(encoders.report, client.reports_stream())

    def check_groups(self) -> Cmd[None]:
        client = CheckGroupClient.new(self.creds, 100)
        return self._from_encoder(encoders.groups, client.list_all())

    def check_status(self) -> Cmd[None]:
        client = CheckStatusClient.new(self.creds, 100)
        return self._from_encoder(encoders.status, client.list_all())

    def check_results(self) -> Cmd[None]:
        client = ChecksClient.new(self.creds, 100, self.old_date, self.now)
        return _emit_stream(
            client.list_ids()
            .bind(
                lambda c: client.list_check_results(c).map(
                    lambda r: IndexedObj(c, r)
                )
            )
            .map(encode_result)
            .transform(chain),
        )


__all__ = [
    "SupportedStreams",
]
