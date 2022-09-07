# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _streams,
)
from ._streams._objs import (
    SupportedStreams,
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
from tap_checkly.api2 import (
    Credentials,
)
from tap_checkly.api2.alert_channels import (
    AlertChannelsClient,
)
from tap_checkly.api2.checks import (
    ChecksClient,
)
from tap_checkly.api import (
    ApiClient,
    Credentials as LegacyCreds,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)
_legacy: Mapping[SupportedStreams, Callable[[ApiClient], Cmd[None]]] = {
    SupportedStreams.CHECKS: _streams.all_checks,
    SupportedStreams.CHECK_GROUPS: _streams.all_chk_groups,
    SupportedStreams.CHECK_STATUS: _streams.all_chk_status,
    SupportedStreams.DASHBOARD: _streams.all_dashboards,
    SupportedStreams.ENV_VARS: _streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: _streams.all_maint_windows,
    SupportedStreams.REPORTS: _streams.all_chk_reports,
    SupportedStreams.SNIPPETS: _streams.all_snippets,
}
OLD_DATE = datetime(1970, 1, 1, tzinfo=timezone.utc)
NOW = datetime.now(tz=timezone.utc)


def emit_stream(creds: Credentials, selection: SupportedStreams) -> Cmd[None]:
    LOG.info("Executing stream: %s", selection)
    if selection is SupportedStreams.CHECK_RESULTS:
        chks_client = ChecksClient.new(creds, 100, OLD_DATE, NOW)
        return _streams.check_results(chks_client)
    if selection is SupportedStreams.ROLLED_RESULTS:
        chks_client = ChecksClient.new(creds, 100, OLD_DATE, NOW)
        return _streams.rolled_results(chks_client)
    elif selection is SupportedStreams.ALERT_CHS:
        chs_client = AlertChannelsClient.new(creds, 100)
        return _streams.alert_chs(chs_client)
    else:
        api = ApiClient.new(LegacyCreds(creds.account, creds.api_key))
        return _legacy[selection](api)


def emit_streams(
    creds: Credentials, targets: FrozenList[SupportedStreams]
) -> Cmd[None]:
    emissions = pure_map(lambda s: emit_stream(creds, s), targets)
    return consume(emissions)
