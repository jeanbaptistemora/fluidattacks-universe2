# Standard library
from typing import (
    Iterator,
    Tuple,
    Union,
)

# Third party libraries
from metaloaders.model import (
    Node,
)

# Local libraries
from aws.model import (
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSS3Acl,
    AWSS3Bucket,
)
from lib_path.common import (
    blocking_get_vulnerabilities_from_iterator,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def create_vulns(
    content: str,
    description_key: str,
    finding: FindingEnum,
    path: str,
    statements_iterator: Iterator[Union[
        AWSIamManagedPolicyArns,
        AWSIamPolicyStatement,
        AWSS3Acl,
        AWSS3Bucket,
        Node,
    ]],
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={finding.value.cwe},
        description=t(
            key=description_key,
            path=path,
        ),
        finding=finding,
        iterator=((
            stmt.start_line if isinstance(stmt, Node) else stmt.line,
            stmt.start_column if isinstance(stmt, Node) else stmt.column,
        ) for stmt in statements_iterator),
        path=path,
    )
