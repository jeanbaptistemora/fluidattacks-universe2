from ._logger import (
    set_logger,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)

__version__ = "0.1.0"

unsafe_unwrap(set_logger(__name__, __version__))


def main() -> None:
    # main placeholder
    pass
