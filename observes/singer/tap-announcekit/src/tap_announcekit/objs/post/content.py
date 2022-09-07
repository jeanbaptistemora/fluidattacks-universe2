# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    PostId,
)


@dataclass(frozen=True)
class PostContent:
    locale_id: str
    title: str
    body: str
    slug: str
    url: str


PostContentObj = IndexedObj[PostId, PostContent]
