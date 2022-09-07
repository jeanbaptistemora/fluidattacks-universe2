# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from code_etl.objs import (
    CommitDataId,
    GroupId,
    User,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)
from typing import (
    FrozenSet,
    Tuple,
)


@dataclass(frozen=True)
class Contribution:
    author: User
    commit_id: CommitDataId


@dataclass(frozen=True)
class ActiveUsersReport:
    data: FrozenDict[User, Contribution]


@dataclass(frozen=True)
class FinalActiveUsersReport:
    data: FrozenDict[User, Tuple[Contribution, FrozenSet[GroupId]]]
