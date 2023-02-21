from aws.model import (
    AWSIamPolicyStatement,
)
from aws.services import (
    ACTIONS_NEW,
)
from collections.abc import (
    Iterator,
)
from contextlib import (
    suppress,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f325.utils import (
    permissive_policy_iterate_vulnerabilities,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents,
)
import re
from typing import (
    Any,
)


def has_write_actions(actions: Any) -> bool:
    result: bool = False
    for entry in actions if isinstance(actions, list) else [actions]:
        with suppress(ValueError):
            service, action = entry.split(":")
            if service in ACTIONS_NEW:
                if (
                    "*" in action
                    and len(
                        [
                            act
                            for act in ACTIONS_NEW[service].get("write", [])
                            if re.match(action.replace("*", ".*"), act)
                            and act
                            not in ACTIONS_NEW[service].get(
                                "wildcard_resource", []
                            )
                        ]
                    )
                    > 0
                ):
                    result = True
                    break
                if action in ACTIONS_NEW[service].get(
                    "write", []
                ) and action not in ACTIONS_NEW[service].get(
                    "wildcard_resource", []
                ):
                    result = True
                    break
    return result


def has_attribute_wildcard(attribute: Any) -> bool:
    result: bool = False
    for value in attribute if isinstance(attribute, list) else [attribute]:
        if value == "*":
            result = True
            break
    return result


def _tfm_iam_has_wildcard_resource_on_write_action_iter_vulns(
    stmts_iterator: Iterator[AWSIamPolicyStatement],
) -> Iterator[AWSIamPolicyStatement]:
    for stmt in stmts_iterator:
        if _policy_has_excessive_permissions(stmt):
            yield stmt


def _policy_has_excessive_permissions(stmt: AWSIamPolicyStatement) -> bool:
    has_excessive_permissions: bool = False
    effect = stmt.data.get("Effect")
    resources = stmt.data.get("Resource")
    actions = stmt.data.get("Action")

    if effect == "Allow":
        if stmt.data.get("NotAction") or stmt.data.get("NotResource"):
            has_excessive_permissions = True
        if has_attribute_wildcard(resources):
            if has_attribute_wildcard(actions) or has_write_actions(actions):
                has_excessive_permissions = True

    return has_excessive_permissions


def tfm_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f325.iam_has_wildcard_resource_on_write_action"
        ),
        iterator=get_cloud_iterator(
            _tfm_iam_has_wildcard_resource_on_write_action_iter_vulns(
                stmts_iterator=iterate_iam_policy_documents(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_WILDCARD_WRITE,
    )


def terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f325_aws.permissive_policy",
        iterator=get_cloud_iterator(
            permissive_policy_iterate_vulnerabilities(
                statements_iterator=iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
        method=MethodsEnum.TFM_PERMISSIVE_POLICY,
    )
