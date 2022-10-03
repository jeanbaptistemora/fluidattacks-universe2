# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._identifier import (
    Identifier,
)
from ._primitive import (
    Primitive,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)


@dataclass(frozen=True)
class Query:
    raw_statement: str
    identifiers: FrozenDict[str, Identifier]
    values: FrozenDict[str, Primitive]

    @staticmethod
    def to_identifiers(
        raw: FrozenDict[str, str]
    ) -> FrozenDict[str, Identifier]:
        return FrozenDict({k: Identifier.from_raw(v) for k, v in raw.items()})

    @property
    def statement(self) -> str:
        try:
            return self.raw_statement.format(
                **{k: v.sql_identifier for k, v in self.identifiers.items()}
            )
        except KeyError as err:
            raise KeyError(
                f"Missing key at statement: {self.raw_statement}"
            ) from err
