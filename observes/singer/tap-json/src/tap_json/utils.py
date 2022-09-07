# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import sys


def log(level: str, msg: str) -> None:
    """Print something to console, the user can see it as progress."""
    print(f"[{level.upper()}]", msg, file=sys.stderr, flush=True)
