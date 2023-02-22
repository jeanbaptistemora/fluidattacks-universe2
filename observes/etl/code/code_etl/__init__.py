from ._logger import (
    set_logger,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)

__version__ = "2.2.4"

unsafe_unwrap(set_logger(__name__, __version__))
