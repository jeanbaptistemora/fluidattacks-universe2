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


class AWSS3Bucket(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSS3Acl(NamedTuple):
    column: int
    data: str
    line: int
