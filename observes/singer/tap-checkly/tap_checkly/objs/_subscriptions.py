# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class AlertChannelId:
    id_int: int


@dataclass(frozen=True)
class ChannelSubscription:
    activated: bool
    channel: AlertChannelId
