import json
import os
from typing import (
    Any,
    Dict,
    List,
    Set,
)

OKTA_DATA: Dict[str, Any] = json.loads(os.environ["OKTA_DATA_RAW"])


def to_dict(*, item: str) -> Dict[str, Any]:
    return {x["id"]: x for x in OKTA_DATA[item]}


def app_groups() -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for app in OKTA_DATA["apps"]:
        for group in OKTA_DATA["groups"]:
            if app["id"] in group["apps"]:
                result.append(
                    {
                        "id": app["id"],
                        "type": app["type"],
                        "group": group["id"],
                    }
                )
    return result


def app_users() -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for app in OKTA_DATA["apps"]:
        for user in OKTA_DATA["users"]:
            if app["id"] in user["apps"]:
                result.append(
                    {
                        "id": app["id"],
                        "type": app["type"],
                        "user": user["id"],
                    }
                )
    return result


def aws_app_roles(*, apps: List[str]) -> Dict[str, List[str]]:
    aws_apps: List[str] = [app for app in apps if "/" in app]
    aws_app_ids: Set[str] = {app.split("/")[0] for app in aws_apps}
    result: Dict[str, List[str]] = {
        aws_app_id: [] for aws_app_id in aws_app_ids
    }
    for aws_app_id in aws_app_ids:
        for aws_app in aws_apps:
            if aws_app_id in aws_app:
                aws_app_role: str = aws_app.split("/")[1]
                result[aws_app_id].append(aws_app_role)
    return result


def aws_group_roles() -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for group in OKTA_DATA["groups"]:
        for app, roles in aws_app_roles(apps=group["apps"]).items():
            result.append(
                {
                    "id": app,
                    "group": group["id"],
                    "roles": roles,
                }
            )
    return result


def aws_user_roles() -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for user in OKTA_DATA["users"]:
        for app, roles in aws_app_roles(apps=user["apps"]).items():
            result.append(
                {
                    "id": app,
                    "user": user["id"],
                    "roles": roles,
                }
            )
    return result


def main() -> None:
    print(
        json.dumps(
            {
                "apps": to_dict(item="apps"),
                "groups": to_dict(item="groups"),
                "rules": to_dict(item="rules"),
                "users": to_dict(item="users"),
                "app_groups": app_groups(),
                "app_users": app_users(),
                "aws_group_roles": aws_group_roles(),
                "aws_user_roles": aws_user_roles(),
            }
        )
    )


if __name__ == "__main__":
    main()
