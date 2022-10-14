# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._subscriptions import (
    ChannelSubscription,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenList,
    Maybe,
)


@dataclass(frozen=True)
class CheckId:
    id_str: str


@dataclass(frozen=True)
class CheckGroup:
    activated: bool
    concurrency: int
    name: str
    alert_channels: FrozenList[ChannelSubscription]
    created_at: datetime
    updated_at: Maybe[datetime]
    double_check: bool
    locations: FrozenList[str]
    muted: bool
    runtime_id: str
    use_global_alert_settings: bool
    # ~apiCheckDefaults~
    # ~browserCheckDefaults~
    # ~alertSettings~
    # ~environmentVariables~
    # ~localSetupScript~
    # ~localTearDownScript~
    # ~privateLocations~
    # ~setupSnippetId~
    # ~tags~
    # ~tearDownSnippetId~
