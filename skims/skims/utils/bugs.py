# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from typing import (
    Dict,
)
from utils.env import (
    guess_environment,
)

# Constants
META: Dict[str, str] = {}


def add_bugsnag_data(**data: str) -> None:
    META.update(data)


def initialize_bugsnag() -> None:
    # Initialization
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        # Ignore multiprocessing SystemExit errors that were flooding Bugsnag
        ignore_classes=["SystemExit"],
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
