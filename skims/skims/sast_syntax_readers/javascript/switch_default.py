# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    yield graph_model.SyntaxStepSwitchLabelDefault(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
    )
