import json
import os
from typing import (
    Any,
    Dict,
    List,
    Set,
)


OKTA_DATA: Dict[str, Any] = json.loads(os.environ['OKTA_DATA'])


def user_groups() -> List[Dict[str, str]]:
    user_groups: List[Dict[str, str]] = []
    for user in OKTA_DATA['users']:
        for group in OKTA_DATA['groups']:
            if user['id'] in group['users']:
                user_groups.append({
                    'id': user['id'],
                    'group': group['id'],
                })
    return user_groups


def app_groups() -> List[Dict[str, str]]:
    app_groups: List[Dict[str, str]] = []
    for app in OKTA_DATA['apps']:
        for group in OKTA_DATA['groups']:
            if app['id'] in group['apps']:
                app_groups.append({
                    'id': app['id'],
                    'type': app['type'],
                    'group': group['id'],
                })
    return app_groups


def app_users() -> List[Dict[str, str]]:
    app_users: List[Dict[str, str]] = []
    for app in OKTA_DATA['apps']:
        for user in OKTA_DATA['users']:
            if app['id'] in user['apps']:
                app_users.append({
                    'id': app['id'],
                    'type': app['type'],
                    'user': user['id'],
                })
    return app_users


def aws_app_roles(apps: List[str]) -> Dict[str, List[str]]:
    aws_apps: List[str] = [app for app in apps if '/' in app]
    aws_app_ids: Set[str] = {app.split('/')[0] for app in aws_apps}
    aws_app_roles: Dict[str, List[str]] = {
        aws_app_id: [] for aws_app_id in aws_app_ids
    }
    for aws_app_id in aws_app_ids:
        for aws_app in aws_apps:
            if aws_app_id in aws_app:
                aws_app_role: str = aws_app.split('/')[1]
                aws_app_roles[aws_app_id].append(aws_app_role)
    return aws_app_roles


def aws_group_roles() -> List[Dict[str, Any]]:
    aws_group_roles: List[Dict[str, Any]] = []
    for group in OKTA_DATA['groups']:
        for app, roles in aws_app_roles(group['apps']).items():
            aws_group_roles.append({
                'id': app,
                'group': group['id'],
                'roles': roles,
            })
    return aws_group_roles


def aws_user_roles() -> List[Dict[str, Any]]:
    aws_user_roles: List[Dict[str, Any]] = []
    for user in OKTA_DATA['users']:
        for app, roles in aws_app_roles(user['apps']).items():
            aws_user_roles.append({
                'id': app,
                'user': user['id'],
                'roles': roles,
            })
    return aws_user_roles
