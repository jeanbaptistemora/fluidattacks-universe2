# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from operator import (
    itemgetter,
)
from typing import (
    Dict,
    NamedTuple,
)
import yaml  # type: ignore


class ValueToAdd(NamedTuple):
    data: Dict[str, int]

    def add(self, element: str) -> None:
        self.data.setdefault(element, 0)
        self.data[element] += 1

    def __str__(self) -> str:
        data = [
            f"{occurrences} - {element}"
            for element, occurrences in sorted(
                self.data.items(),
                key=itemgetter(1),
                reverse=True,
            )
        ]
        return yaml.safe_dump(data)
