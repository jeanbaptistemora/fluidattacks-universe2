import ast
from contextlib import (
    suppress,
)
from dast.aws import (
    services,
)
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    Vulnerability,
)
import re
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Pattern,
    Tuple,
)
from zone import (
    t,
)


def service_is_present_action(action: str, service: str) -> bool:
    """Check if a service is present in an action."""
    success = False
    with suppress(KeyError):
        if isinstance(action, List):
            success = service in [act.split(":")[0] for act in action]
        elif action == "*":
            success = True
        else:
            success = action.split(":")[0] == service
    return success


async def iam_has_privileges_over_iam(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    method = core_model.MethodsEnum.AWS_IAM_HAS_PRIVILEGES_OVER_IAM
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            policy_version: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": policy["Arn"],
                    "VersionId": policy["DefaultVersionId"],
                },
            )
            policy_names = policy_version.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if item["Effect"] == "Allow" and service_is_present_action(
                        item["Action"], "iam"
                    ):
                        locations = [
                            *locations,
                            Location(
                                access_patterns=(),
                                arn=(f"{policy['Arn']}"),
                                values=(
                                    policy_statements[index]["Effect"],
                                    policy_statements[index]["Action"],
                                ),
                                description=t(
                                    "src.lib_path.f325."
                                    "iam_has_privileges_over_iam"
                                ),
                            ),
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy_names,
                ),
            )

    return vulns


def iterate_kms_has_master_keys_exposed_to_everyone(
    key_policy: Dict[str, Any], alias: Dict[str, Any]
) -> List[Location]:
    locations: List[Location] = []
    for index, item in enumerate(key_policy["Statement"]):
        if item["Principal"]["AWS"] == "*" and "Condition" not in item:
            locations = [
                *locations,
                Location(
                    access_patterns=(f"/Statement/{index}/Principal/AWS",),
                    arn=(f"{alias['AliasArn']}"),
                    values=(item["Principal"]["AWS"],),
                    description=t(
                        "src.lib_path.f325."
                        "kms_key_has_master_keys_exposed_to_everyone"
                    ),
                ),
            ]
    return locations


async def kms_has_master_keys_exposed_to_everyone(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="kms",
        function="list_aliases",
    )
    aliases = response.get("Aliases", []) if response else []
    method = core_model.MethodsEnum.AWS_KMS_HAS_MASTER_KEYS_EXPOSED_TO_EVERYONE
    vulns: core_model.Vulnerabilities = ()
    if aliases:
        for alias in aliases:
            with suppress(KeyError):
                list_key_policies: Dict[str, Any] = await run_boto3_fun(
                    credentials,
                    service="kms",
                    function="list_key_policies",
                    parameters={
                        "KeyId": alias["TargetKeyId"],
                    },
                )
                policy_names = list_key_policies.get("PolicyNames", {})
                for policy in policy_names:
                    get_key_policy: Dict[str, Any] = await run_boto3_fun(
                        credentials,
                        service="kms",
                        function="get_key_policy",
                        parameters={
                            "KeyId": alias["TargetKeyId"],
                            "PolicyName": policy,
                        },
                    )
                    key_string = get_key_policy["Policy"]
                    key_policy = ast.literal_eval(key_string)

                    locations = (
                        iterate_kms_has_master_keys_exposed_to_everyone(
                            key_policy, alias
                        )
                    )

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=key_policy,
                        ),
                    )

    return vulns


def resource_all(resource: Any) -> bool:
    """Check if an action is permitted for any resource."""
    if isinstance(resource, List):
        success = any(map(resource_all, resource))
    elif isinstance(resource, str):
        success = resource == "*"
    else:
        success = any(resource_all(i) for i in dict(resource).values())

    return success


def force_list(obj: Any) -> List[Any]:
    """Wrap the element in a list, or if list, leave it intact."""
    if not obj:
        ret = []
    elif isinstance(obj, List):
        ret = obj
    else:
        ret = [obj]
    return ret


def policy_actions_has_privilege(action: List, privilege: str) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = services.ACTIONS
    success = False
    with suppress(KeyError):
        if action == ["*"]:
            success = True
        else:
            actions = []
            for act in action:
                serv, act = act.split(":")
                if act.startswith("*"):
                    actions.append(True)
                else:
                    act = act[: act.index("*")] if act.endswith("*") else act
                    actions.append(
                        act in write_actions.get(serv, {})[privilege]
                    )
            success = any(actions)
    return success


def get_locations(
    policy_statements: List, policy: Dict[str, Any]
) -> List[Location]:
    locations: List[Location] = []
    for item in policy_statements:
        item = ast.literal_eval(str(item))
        if (
            item["Effect"] == "Allow"
            and "Resource" in item
            and resource_all(item["Resource"])
        ):
            actions = force_list(item["Action"])
            if policy_actions_has_privilege(actions, "write"):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(),
                        arn=(f"{policy['Arn']}"),
                        values=(
                            item["Effect"],
                            item["Resource"],
                            item["Action"],
                        ),
                        description=t(
                            "src.lib_path.f325."
                            "iam_has_wildcard_resource_on_write_action"
                        ),
                    ),
                ]

    return locations


async def iam_has_wildcard_resource_on_write_action(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    method = (
        core_model.MethodsEnum.AWS_IAM_HAS_WILDCARD_RESOURCE_IN_WRITE_ACTION
    )

    policies = response.get("Policies", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            pol_ver: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )
            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            locations = get_locations(policy_statements, policy)

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy_statements,
                ),
            )

    return vulns


def _get_wildcard_nodes(
    act_res: List,
    pattern: Pattern,
    policy: Dict[str, Any],
    policy_statements: List[Dict[str, Any]],
    index: int,
) -> List[Location]:
    locations: List[Location] = []
    action = policy_statements[index]["Action"]
    for index_act, act in enumerate(act_res):
        if pattern.match(act):
            locations = [
                *locations,
                Location(
                    access_patterns=(),
                    arn=(f"{policy['Arn']}"),
                    values=(
                        policy_statements[index]["Effect"],
                        action[index_act]
                        if isinstance(action, List)
                        else action,
                    ),
                    description=t(
                        "src.lib_path.f325.iam_is_policy_miss_configured"
                    ),
                ),
            ]
    return locations


def _is_statement_miss_configured(
    stmt: Dict[str, Any],
    index: int,
    policy: Dict[str, Any],
    policy_statements: List[Dict[str, Any]],
) -> Any:
    wildcard_action: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
    effect = stmt.get("Effect")
    no_action = stmt.get("NotAction")
    no_resource = stmt.get("NotResource")
    locations: List[Location] = []
    if effect == "Allow":
        if no_action and isinstance(no_action, List):
            locations = [
                *locations,
                Location(
                    access_patterns=(),
                    arn=(f"{policy['Arn']}"),
                    values=(no_action,),
                    description=t(
                        "src.lib_path.f325.iam_is_policy_miss_configured"
                    ),
                ),
            ]

        if no_resource and isinstance(no_resource, List):
            locations = [
                *locations,
                Location(
                    access_patterns=(),
                    arn=(f"{policy['Arn']}"),
                    values=(no_resource,),
                    description=t(
                        "src.lib_path.f325.iam_is_policy_miss_configured"
                    ),
                ),
            ]

        action = stmt.get("Action")
        if action:
            locations = [
                *locations,
                *_get_wildcard_nodes(
                    action if isinstance(action, List) else [action],
                    wildcard_action,
                    policy,
                    policy_statements,
                    index,
                ),
            ]
    return locations


async def iam_is_policy_miss_configured(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    method = core_model.MethodsEnum.AWS_IAM_IS_POLICY_MISS_CONFIGURED

    policies = response.get("Policies", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            pol_ver: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )
            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, policy_statement in enumerate(policy_statements):
                locations = [
                    *locations,
                    *_is_statement_miss_configured(
                        policy_statement, index, policy, policy_statements
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy_names,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    kms_has_master_keys_exposed_to_everyone,
    iam_has_privileges_over_iam,
    iam_has_wildcard_resource_on_write_action,
    iam_is_policy_miss_configured,
)
