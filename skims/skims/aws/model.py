# Standard library
from typing import (
    Any,
    NamedTuple,
)


class AWSIamPolicyStatement(NamedTuple):
    column: int
    data: Any
    line: int
