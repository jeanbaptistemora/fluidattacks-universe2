from ._logger import (
    set_logger,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)

__version__ = "3.0.0"

unsafe_unwrap(set_logger(__name__, __version__))
