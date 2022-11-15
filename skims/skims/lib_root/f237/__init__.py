# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f237.dart import (
    has_print_statements as dart_has_print_statements,
)
from lib_root.f237.java import (
    has_print_statements as java_has_print_statements,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F237
QUERIES: graph_model.Queries = (
    (FINDING, java_has_print_statements),
    (FINDING, dart_has_print_statements),
)
