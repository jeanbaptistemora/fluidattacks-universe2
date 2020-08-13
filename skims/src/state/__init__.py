# Standard library
from os import (
    makedirs,
)
from os.path import (
    expanduser,
)

# Constants
STATE_FOLDER: str = expanduser('~/.skims')

# Side effects
makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)
