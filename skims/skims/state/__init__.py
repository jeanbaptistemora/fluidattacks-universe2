# Standard library
from os import (
    makedirs,
)
import os
from os.path import (
    expanduser,
)

# Constants
STATE_FOLDER: str = expanduser('~/.skims')
STATE_FOLDER_DEBUG: str = os.path.join(STATE_FOLDER, 'debug')

# Side effects
makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)
makedirs(STATE_FOLDER_DEBUG, mode=0o700, exist_ok=True)
