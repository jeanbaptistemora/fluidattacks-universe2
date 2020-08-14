# Standard library
from typing import (
    NamedTuple,
)

# Containers
_SCALE = NamedTuple('Scale', [
    ('more_passive', str),
    ('passive', str),
    ('neutral', str),
    ('agressive', str),
    ('more_agressive', str),
])

# https://coolors.co/323031-084c61-177e89-ffc857-db3a34
RISK = _SCALE(
    more_passive='#323031',
    passive='#084c61',
    neutral='#177e89',
    agressive='#ffc857',
    more_agressive='#db3a34',
)

# https://coolors.co/233d4d-619b8a-a1c181-fcca46-fe7f2d
TREATMENT = _SCALE(
    more_passive='#233d4d',
    passive='#619b8a',
    neutral='#a1c181',
    agressive='#fcca46',
    more_agressive='#fe7f2d',
)

# https://coolors.co/abb8b6-839794-6f8683-657e7b-5b7572
OTHER = _SCALE(
    more_passive='#abb8b6',
    passive='#839794',
    neutral='#6f8683',
    agressive='#657e7b',
    more_agressive='#5b7572',
)
