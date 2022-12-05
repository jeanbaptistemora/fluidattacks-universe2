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

GRAY_JET: str = "#323031"
EXPOSURE: str = "#ac0a17"
VULNERABILITIES_COUNT: str = "#cc6699"
TYPES_COUNT: str = "#7f0540"
OTHER_COUNT: str = "#fda6ab"
