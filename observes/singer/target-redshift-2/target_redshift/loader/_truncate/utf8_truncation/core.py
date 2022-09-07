# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Result,
    ResultE,
)


@dataclass(frozen=True)
class PrimaryByteLayer(Enum):
    LAYER_0 = "LAYER_0"
    LAYER_1 = "LAYER_1"
    LAYER_2 = "LAYER_2"
    LAYER_3 = "LAYER_3"


@dataclass(frozen=True)
class _PrimaryByte:
    byte: int
    layer: PrimaryByteLayer


@dataclass(frozen=True)
class PrimaryByte(_PrimaryByte):
    def __init__(self, inner: _PrimaryByte) -> None:
        super().__init__(inner.byte, inner.layer)


class NotAPrimaryByte(Exception):
    pass


def new_primary_byte(byte: int) -> ResultE[PrimaryByte]:
    if (byte & 0b10000000) == 0:
        return Result.success(
            PrimaryByte(_PrimaryByte(byte, PrimaryByteLayer.LAYER_0))
        )
    if (byte & 0b11100000) == 0b11000000:
        return Result.success(
            PrimaryByte(_PrimaryByte(byte, PrimaryByteLayer.LAYER_1))
        )
    if (byte & 0b11110000) == 0b11100000:
        return Result.success(
            PrimaryByte(_PrimaryByte(byte, PrimaryByteLayer.LAYER_2))
        )
    if (byte & 0b11111000) == 0b11110000:
        return Result.success(
            PrimaryByte(_PrimaryByte(byte, PrimaryByteLayer.LAYER_3))
        )
    return Result.failure(NotAPrimaryByte())


@dataclass(frozen=True)
class _SecondaryByte:
    byte: int


@dataclass(frozen=True)
class SecondaryByte(_SecondaryByte):
    def __init__(self, inner: _SecondaryByte) -> None:
        super().__init__(inner.byte)


class NotASecondaryByte(Exception):
    pass


def new_secondary_byte(byte: int) -> ResultE[SecondaryByte]:
    if (byte & 0b11000000) == 0b10000000:
        return Result.success(SecondaryByte(_SecondaryByte(byte)))
    return Result.failure(NotASecondaryByte())


def secondary_bytes_of(byte: PrimaryByte) -> int:
    if byte.layer is PrimaryByteLayer.LAYER_0:
        return 0
    if byte.layer is PrimaryByteLayer.LAYER_1:
        return 1
    if byte.layer is PrimaryByteLayer.LAYER_2:
        return 2
    if byte.layer is PrimaryByteLayer.LAYER_3:
        return 3
    raise NotImplementedError(f"Missing case for {byte.layer}")
