from model import (
    core_model,
)
from operator import (
    itemgetter,
)
from typing import (
    Dict,
    NamedTuple,
)
import yaml  # type: ignore


class ValueToAdd(NamedTuple):
    data: Dict[core_model.FindingEnum, Dict[str, int]]

    def add(self, finding: core_model.FindingEnum, element: str) -> None:
        self.data.setdefault(finding, {})
        self.data[finding].setdefault(element, 0)
        self.data[finding][element] += 1

    def __str__(self) -> str:
        data = {
            finding.name: [
                f"{occurrences} - {element}"
                for element, occurrences in sorted(
                    finding_data.items(),
                    key=itemgetter(1),
                    reverse=True,
                )
            ]
            for finding, finding_data in self.data.items()
        }
        return yaml.safe_dump(data)


VALUE_TO_ADD = ValueToAdd({})
