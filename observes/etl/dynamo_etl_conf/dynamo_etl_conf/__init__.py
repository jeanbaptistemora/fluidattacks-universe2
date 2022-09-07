# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._utils import (
    get_log,
)
import logging

__version__ = "1.0.2"
LOG = get_log(__name__, logging.DEBUG)
