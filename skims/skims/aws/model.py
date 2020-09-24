# Standard library
from typing import (
    Any,
    List,
    NamedTuple,
    Optional,
)


class AWSIamPolicyStatement(NamedTuple):
    column: int
    data: Any
    line: int


class AWSIamManagedPolicyArns(NamedTuple):
    column: int
    data: Optional[List[str]]
    line: int
