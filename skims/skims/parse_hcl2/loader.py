# Standard library
from typing import (
    Any,
)

# Third party libraries
from hcl2.transformer import (
    DictTransformer,
)
from hcl2.lark_parser import (
    DATA,
    Lark_StandAlone,
)
import lark


# Side effects
DATA['options']['propagate_positions'] = True


class HCL2Builder(  # pylint: disable=too-few-public-methods
    lark.Transformer,  # type: ignore
):

    def __init__(self) -> None:
        self.transformer = DictTransformer()
        super().__init__()


def load(stream: str) -> Any:
    loader = Lark_StandAlone(HCL2Builder())

    return loader.parse(stream)
