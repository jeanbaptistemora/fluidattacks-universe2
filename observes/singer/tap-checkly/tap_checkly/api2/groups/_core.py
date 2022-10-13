# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenList,
)
from tap_checkly.api2.alert_channels import (
    ChannelSubscription,
)
from tap_checkly.api2.id_objs import (
    IndexedObj,
)


@dataclass(frozen=True)
class CheckGroupId:
    raw_id: int


@dataclass(frozen=True)
class CheckGroup:
    activated: bool
    # ~apiCheckDefaults~
    # ~browserCheckDefaults~
    concurrency: int
    name: str
    alert_channels: FrozenList[ChannelSubscription]
    # ~alertSettings~
    created_at: datetime
    updated_at: datetime
    double_check: bool
    # ~environmentVariables~
    # ~localSetupScript~
    # ~localTearDownScript~
    locations: FrozenList[str]
    muted: bool
    # ~privateLocations~
    runtime_id: str
    # ~setupSnippetId~
    # ~tags~
    # ~tearDownSnippetId~
    use_global_alert_settings: bool


CheckGroupObj = IndexedObj[CheckGroupId, CheckGroup]
