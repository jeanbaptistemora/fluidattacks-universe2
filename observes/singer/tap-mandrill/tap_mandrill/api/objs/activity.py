# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
    ResultE,
)
from tap_mandrill import (
    _utils,
)


@dataclass(frozen=True)
class _MainData:
    date: datetime
    receiver: str  # e-mail
    sender: str  # e-mail
    subject: str
    status: str

    @staticmethod
    def decode(raw: FrozenDict[str, str]) -> ResultE[_MainData]:
        date = _utils.get_item(raw, "Date").bind(_utils.isoparse)
        return _utils.get_item(raw, "Status").bind(
            lambda status: _utils.get_item(raw, "Email Address").bind(
                lambda receiver: _utils.get_item(raw, "Sender").bind(
                    lambda sender: _utils.get_item(raw, "Subject").bind(
                        lambda subject: date.map(
                            lambda d: _MainData(
                                d, receiver, sender, subject, status
                            )
                        )
                    )
                )
            )
        )


@dataclass(frozen=True)
class _SecondaryData:
    tags: str
    subaccount: str
    opens: int
    clicks: int
    bounce: str

    @staticmethod
    def decode(raw: FrozenDict[str, str]) -> ResultE[_SecondaryData]:
        opens = _utils.get_item(raw, "Opens").bind(_utils.to_int)
        clicks = _utils.get_item(raw, "Clicks").bind(_utils.to_int)
        return _utils.get_item(raw, "Tags").bind(
            lambda tags: _utils.get_item(raw, "Subaccount").bind(
                lambda sub: _utils.get_item(raw, "Bounce Detail").bind(
                    lambda bounce: opens.bind(
                        lambda ops: clicks.map(
                            lambda clks: _SecondaryData(
                                tags, sub, ops, clks, bounce
                            )
                        )
                    )
                )
            )
        )


@dataclass(frozen=True)
class Activity:
    date: datetime
    receiver: str
    sender: str
    subject: str
    status: str
    tags: str
    subaccount: str
    opens: int
    clicks: int
    bounce: str

    @staticmethod
    def _build_activity(main: _MainData, sec: _SecondaryData) -> Activity:
        return Activity(
            main.date,
            main.receiver,
            main.sender,
            main.subject,
            main.status,
            sec.tags,
            sec.subaccount,
            sec.opens,
            sec.clicks,
            sec.bounce,
        )

    @classmethod
    def decode(cls, raw: FrozenDict[str, str]) -> ResultE[Activity]:
        return _MainData.decode(raw).bind(
            lambda m: _SecondaryData.decode(raw).map(
                lambda s: cls._build_activity(m, s)
            )
        )
