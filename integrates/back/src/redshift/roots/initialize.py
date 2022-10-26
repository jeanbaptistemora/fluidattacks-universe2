# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..operations import (
    SCHEMA_NAME,
)
import logging

LOGGER = logging.getLogger(__name__)
CODE_LANGUAGES_TABLE: str = f"{SCHEMA_NAME}.roots_code_languages"
METADATA_TABLE: str = f"{SCHEMA_NAME}.roots_metadata"
