# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_DB_MODEL_PATH,
)
from dynamodb.tables import (
    load_tables,
)
import json

with open(FI_DB_MODEL_PATH, mode="r", encoding="utf-8") as file:
    TABLE = load_tables(json.load(file))[0]
