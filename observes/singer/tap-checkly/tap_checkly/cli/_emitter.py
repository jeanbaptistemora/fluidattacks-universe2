# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
    timezone,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.pure_iter.transform import (
    consume,
)
import logging
from tap_checkly.api import (
    Credentials,
)
from tap_checkly.state import (
    EtlState,
)
from tap_checkly.streams import (
    Streams,
    SupportedStreams,
)

LOG = logging.getLogger(__name__)
OLD_DATE = datetime(1970, 1, 1, tzinfo=timezone.utc)
NOW = datetime.now(tz=timezone.utc)


@dataclass(frozen=True)
class Emitter:
    state: EtlState
    creds: Credentials

    def emit_stream(self, selection: SupportedStreams) -> Cmd[None]:
        _streams = Streams(self.creds, OLD_DATE, NOW)

        def stream_mapper(
            item: SupportedStreams,
        ) -> Cmd[None]:  # return type should be Cmd[None]
            if item is SupportedStreams.CHECKS:
                return _streams.all_checks()
            if item is SupportedStreams.CHECK_GROUPS:
                return _streams.check_groups()
            if item is SupportedStreams.CHECK_RESULTS:
                return _streams.check_results(self.state)
            if item is SupportedStreams.ALERT_CHS:
                return _streams.alert_chs()
            if item is SupportedStreams.CHECK_STATUS:
                return _streams.check_status()
            if item is SupportedStreams.REPORTS:
                return _streams.check_reports()

        def _execute(item: SupportedStreams) -> Cmd[None]:
            info = Cmd.from_cmd(lambda: LOG.info("Executing stream: %s", item))
            return info + stream_mapper(item)

        return _execute(selection)

    def emit_streams(self, targets: FrozenList[SupportedStreams]) -> Cmd[None]:
        emissions = pure_map(self.emit_stream, targets)
        return consume(emissions)
