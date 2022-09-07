# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from itertools import (
    repeat,
)


def boxify(
    *,
    width_to_height_ratio: int = 3,
    string: str,
) -> str:
    lines: list[str] = string.splitlines()

    width, height = max(map(len, lines + [""])), len(lines)

    missing_height: int = width // width_to_height_ratio - height

    filling: list[str] = list(repeat("", missing_height // 2))

    return "\n".join(filling + lines + filling)
