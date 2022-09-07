# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepsLazy,
    SyntaxStepSymbolLookup,
    SyntaxStepTemplateString,
)
import re
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    List,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    pattern = re.compile(r"\$\{([a-zA-z_]*)\}")
    text = args.graph.nodes[args.n_id]["label_text"]
    result: List[str] = pattern.findall(text)
    identifiers = [
        SyntaxStepSymbolLookup(
            meta=SyntaxStepMeta.default(args.n_id),
            symbol=identifier,
        )
        for identifier in result
    ]
    yield SyntaxStepTemplateString(
        meta=SyntaxStepMeta.default(args.n_id, [identifiers])
    )
