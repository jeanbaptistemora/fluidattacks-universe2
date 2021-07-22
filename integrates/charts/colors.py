from typing import (
    NamedTuple,
)

# Containers
_SCALE = NamedTuple(
    "Scale",
    [
        ("more_passive", str),
        ("passive", str),
        ("neutral", str),
        ("agressive", str),
        ("more_agressive", str),
    ],
)

# https://coolors.co/009044-084c61-177e89-ffc857-db3a34
RISK = _SCALE(
    more_passive="#009044",
    passive="#084c61",
    neutral="#177e89",
    agressive="#ffc857",
    more_agressive="#db3a34",
)

# https://coolors.co/fdd25e-f99a30-f8903a-f77d26-f46201
TREATMENT = _SCALE(
    more_passive="#fdd25e",
    passive="#f99a30",
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
