# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)

# Containers
_SCALE = NamedTuple(
    "_SCALE",
    [
        ("more_passive", str),
        ("passive", str),
        ("neutral", str),
        ("agressive", str),
        ("more_agressive", str),
    ],
)

_SEVERITYSCALE = NamedTuple(
    "_SEVERITYSCALE",
    [
        ("low", str),
        ("medium", str),
        ("high", str),
        ("critical", str),
    ],
)

# https://coolors.co/33cc99-084c61-177e89-ffc857-da1e28
RISK = _SCALE(
    more_passive="#33cc99",
    passive="#084c61",
    neutral="#177e89",
    agressive="#ffc857",
    more_agressive="#da1e28",
)

# https://coolors.co/fdd25e-ffcc33-f8903a-f77d26-f46201
TREATMENT = _SCALE(
    more_passive="#fdd25e",
    passive="#ffcc33",
    neutral="#f8903a",
    agressive="#f77d26",
    more_agressive="#f46201",
)

# https://coolors.co/abb8b6-839794-6f8683-657e7b-5b7572
OTHER = _SCALE(
    more_passive="#abb8b6",
    passive="#839794",
    neutral="#6f8683",
    agressive="#657e7b",
    more_agressive="#5b7572",
)

# https://coolors.co/ffce00-ffa031-e00000-8b0000
SEVERITY = _SEVERITYSCALE(
    low="#ffce00",
    medium="#ffa031",
    high="#e00000",
    critical="#8b0000",
)

GRAY_JET: str = "#323031"
