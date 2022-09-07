# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_zoho_crm.api.common import (
    DataPageInfo,
)
from typing import (
    List,
    NamedTuple,
)


class UserType(Enum):
    ANY = "AllUsers"


class UsersDataPage(NamedTuple):
    data: List[JsonObj]
    info: DataPageInfo
