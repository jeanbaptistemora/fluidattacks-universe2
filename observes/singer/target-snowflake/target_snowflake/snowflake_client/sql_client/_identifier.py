# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
    ResultE,
)
import re


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class UnquotedIdentifier:
    _inner: _Private
    sql_identifier: str

    @staticmethod
    def new(identifier: str) -> ResultE[UnquotedIdentifier]:
        pattern = "^[A-Za-z_][\\w$]+$"
        match = re.match(pattern, identifier)
        return (
            Maybe.from_optional(match)
            .map(lambda m: m.group(0))
            .map(lambda i: UnquotedIdentifier(_Private(), i.upper()))
            .to_result()
            .alt(
                lambda _: Exception(
                    f"Invalid UnquotedIdentifier i.e. {identifier}"
                )
            )
        )


@dataclass(frozen=True)
class QuotedIdentifier:
    _inner: _Private
    sql_identifier: str

    @staticmethod
    def new(identifier: str) -> QuotedIdentifier:
        escaped = identifier.replace('"', '""')
        return QuotedIdentifier(_Private(), '"' + escaped + '"')


@dataclass(frozen=True)
class Identifier:
    _inner: _Private
    sql_identifier: str

    @staticmethod
    def from_quoted(item: QuotedIdentifier) -> Identifier:
        return Identifier(_Private(), item.sql_identifier)

    @staticmethod
    def from_unquoted(item: UnquotedIdentifier) -> Identifier:
        return Identifier(_Private(), item.sql_identifier)

    @classmethod
    def from_raw(cls, item: str) -> Identifier:
        return (
            UnquotedIdentifier.new(item)
            .map(cls.from_unquoted)
            .or_else_call(lambda: cls.from_quoted(QuotedIdentifier.new(item)))
        )
