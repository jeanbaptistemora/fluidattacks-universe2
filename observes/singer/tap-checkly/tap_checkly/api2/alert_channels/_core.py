# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from tap_checkly.objs import (
    AlertChannel,
    AlertChannelId,
    ChannelSubscription,
    IndexedObj,
)

AlertChannelObj = IndexedObj[AlertChannelId, AlertChannel]
__all__ = [
    "AlertChannelId",
    "AlertChannel",
    "ChannelSubscription",
]
