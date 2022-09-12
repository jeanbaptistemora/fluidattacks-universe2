# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._logger import (
    set_logger,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)

__version__ = "1.0.0"

unsafe_unwrap(set_logger(__name__, __version__))
