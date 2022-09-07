# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb.types import (
    PageInfo,
)
from typing import (
    Any,
    NamedTuple,
)

Item = dict[str, Any]


class SearchResponse(NamedTuple):
    items: tuple[Item, ...]
    page_info: PageInfo
