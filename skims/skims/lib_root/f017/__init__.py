# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f017.c_sharp import (
    jwt_signed as c_sharp_jwt_signed,
    verify_decoder as c_sharp_verify_decoder,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F017
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_jwt_signed),
    (FINDING, c_sharp_verify_decoder),
)
