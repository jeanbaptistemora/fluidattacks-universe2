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
