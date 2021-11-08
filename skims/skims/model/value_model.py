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


VALUE_TO_ADD = ValueToAdd({})
