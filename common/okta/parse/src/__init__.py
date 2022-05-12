import json
import os
import sys
from typing import (
    Any,
)

OKTA_DATA_RAW: dict[str, Any] = {
    "apps": json.loads(os.environ["OKTA_DATA_RAW_APPS"]),
    "groups": json.loads(os.environ["OKTA_DATA_RAW_GROUPS"]),
    "rules": json.loads(os.environ["OKTA_DATA_RAW_RULES"]),
    "users": json.loads(os.environ["OKTA_DATA_RAW_USERS"]),
}


def to_dict(*, item: str) -> dict[str, Any]:
    return {x["id"]: x for x in OKTA_DATA_RAW[item]}


def app_groups() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for app in OKTA_DATA_RAW["apps"]:
        for group in OKTA_DATA_RAW["groups"]:
            if app["id"] in group["apps"]:
                result.append(
                    {
                        "id": app["id"],
                        "type": app["type"],
                        "group": group["id"],
                    }
                )
    return result


def app_users() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for app in OKTA_DATA_RAW["apps"]:
        for user in OKTA_DATA_RAW["users"]:
            if app["id"] in user["apps"]:
                result.append(
                    {
                        "id": app["id"],
                        "type": app["type"],
                        "user": user["id"],
                    }
                )
    return result


def aws_app_roles(*, apps: list[str]) -> dict[str, list[str]]:
    aws_apps: list[str] = [app for app in apps if "/" in app]
    aws_app_ids: set[str] = {app.split("/")[0] for app in aws_apps}
    result: dict[str, list[str]] = {
        aws_app_id: [] for aws_app_id in aws_app_ids
    }
    for aws_app_id in aws_app_ids:
        for aws_app in aws_apps:
            if aws_app_id in aws_app:
                aws_app_role: str = aws_app.split("/")[1]
                result[aws_app_id].append(aws_app_role)
    return result


def aws_group_roles() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for group in OKTA_DATA_RAW["groups"]:
        for app, roles in aws_app_roles(apps=group["apps"]).items():
            result.append(
                {
                    "id": app,
                    "group": group["id"],
                    "roles": roles,
                }
            )
    return result


def aws_user_roles() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for user in OKTA_DATA_RAW["users"]:
        for app, roles in aws_app_roles(apps=user["apps"]).items():
            result.append(
                {
                    "id": app,
                    "user": user["id"],
                    "roles": roles,
                }
            )
    return result


def main(data_type: str) -> None:
    response: Any = None

    if data_type in ["apps", "groups", "rules", "users"]:
        response = to_dict(item=data_type)
    else:
        response = globals()[data_type]()

    print(
        json.dumps(
            response,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main(sys.argv[1].lower())
