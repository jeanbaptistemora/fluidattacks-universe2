from aws.model import (
    AWSIamManagedPolicy,
)
from lib_path.common import (
    get_line_by_extension,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
)
import re
from typing import (
    Any,
    Iterator,
    List,
    Pattern,
    Union,
)

WILDCARD_ACTION: Pattern = re.compile(r"^((\*)|(\w+:\*))$")


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


def check_type(
    stmt: Any, file_ext: str, method: MethodsEnum
) -> Iterator[Node]:

    if (
        not_actions := stmt.inner.get("NotAction")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_ACTION:
        yield AWSIamManagedPolicy(
            column=not_actions.start_column,
            data=not_actions.data,
            line=get_line_by_extension(not_actions.start_line, file_ext),
        ) if isinstance(not_actions.raw, List) else not_actions

    if (
        not_princ := stmt.inner.get("NotPrincipal")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_PRINCIPAL:
        yield AWSIamManagedPolicy(  # type: ignore
            column=not_princ.start_column,
            data=not_princ.data,
            line=get_line_by_extension(not_princ.start_line, file_ext),
        )

    if (
        actions := stmt.inner.get("Action")
    ) and method == MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION:
        yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def check_assume_role_policies(
    assume_role_policy: Node, file_ext: str, method: MethodsEnum
) -> Iterator[Node]:
    statements = (
        assume_role_policy.inner.get("Statement")
        if hasattr(assume_role_policy.inner, "get")
        else None
    )
    for stmt in statements.data if statements else []:
        if (
            hasattr(stmt.inner, "get")
            and (effect := stmt.inner.get("Effect"))
            and effect.raw != "Allow"
        ):
            continue
        yield from check_type(stmt, file_ext, method)


def iam_trust_policies_checks(
    file_ext: str,
    iam_iterator: Iterator[Node],
    method: MethodsEnum,
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            yield from check_assume_role_policies(
                assume_role_policy,
                file_ext,
                method,
            )
