# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f354.java import (
    insecure_file_upload_size,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F354
QUERIES: graph_model.Queries = ((FINDING, insecure_file_upload_size),)
