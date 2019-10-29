#!/usr/bin/env python3
"""Mirror customer repositories to Gitlab."""

import os
import re
import json
import time
import urllib.parse

from glob import glob
from typing import Tuple, Any

import urllib3

API_URL: str = "https://gitlab.com/api/v4"
TARPIT_TIME: float = 10.0


def get_key(key: str) -> str:
    """Get a key from vault."""
    return os.popen(f'vault read -field={key} secret/serves').read()


def _success(status: int) -> bool:
    """Return True if the status is between 200 and 299 inclusive."""
    return 200 <= status <= 299


def _url_escape(name: str) -> str:
    name = str(name)
    return urllib.parse.quote(name, safe='')


def _valid_path(path: str) -> str:
    path = str(path)
    return re.sub(r'[^a-zA-Z0-9_]+', '-', path).lower()


def _do_request(
        token: str, method: str, resource: str) -> Tuple[int, Any]:
    """Request a resource, return status and response."""
    print(method, resource)

    http = urllib3.PoolManager()
    resp = http.request(method, resource, headers={"PRIVATE-TOKEN": token})

    status, response = resp.status, None
    if _success(status):
        response = resp.data.decode()

    print(status, resp.data.decode())

    return status, response


def do_request(token: str, method: str, resource: str) -> Tuple[int, Any]:
    """Request a resource, return status and response."""
    status, response = _do_request(token, method, resource)
    for _ in range(2):
        if response:
            break
        time.sleep(TARPIT_TIME)
        status, response = _do_request(token, method, resource)
    return status, response


def get_group(token: str, group_id: str) -> Tuple[int, Any]:
    """Get a group."""
    print('get_group', 'group_id', group_id)
    resource = f"{API_URL}/groups/{_url_escape(group_id)}"
    status, response = do_request(token, "GET", resource)
    return status, json.loads(response)["id"] if response else None


def create_group(token: str, parent_id: str, name: str) -> Tuple[int, Any]:
    """Create a group into parent."""
    print('create_group', 'parent_id', parent_id, 'name', name)
    resource = (
        f"{API_URL}/groups"
        f"?name={_url_escape(name)}"
        f"&path={_valid_path(name)}"
        f"&parent_id={_url_escape(parent_id)}")
    status, response = do_request(token, "POST", resource)
    return status, json.loads(response)["id"] if response else None


def delete_group(token: str, group_id: str) -> Tuple[int, Any]:  # noqa
    """Delete a group if exist."""
    print('delete_group', 'group_id', group_id)
    resource = f"{API_URL}/groups/{_url_escape(group_id)}"
    status, response = do_request(token, "DELETE", resource)
    return status, response


def get_project(token: str, project_id: str) -> Tuple[int, Any, Any]:
    """Delete a project if exist."""
    print('get_project', 'project_id', project_id)
    resource = f"{API_URL}/projects/{_url_escape(project_id)}"
    status, response = do_request(token, "GET", resource)
    proj_id = json.loads(response)["id"] if response else None
    proj_url = json.loads(response)["http_url_to_repo"] if response else None
    return status, proj_id, proj_url


def delete_project(token: str, project_id: str) -> Tuple[int, Any]:  # noqa
    """Delete a project if exist."""
    print('delete_project', 'project_id', project_id)
    resource = f"{API_URL}/projects/{_url_escape(project_id)}"
    status, response = do_request(token, "DELETE", resource)
    return status, response


def list_groups_in_group(token: str, group_id: str) -> Tuple[int, Any]:  # noqa
    """List groups in a group."""
    print('list_groups_in_group', 'group_id', group_id)
    group_ids: Any = []
    resource = f"{API_URL}/groups/{_url_escape(group_id)}/subgroups"
    status, response = do_request(token, "GET", resource)
    if response:
        group_ids.extend(group["id"] for group in json.loads(response))
    return status, group_ids


def list_projects_in_group(  # noqa
        token: str, group_id: str) -> Tuple[int, Any]:
    """List projects in a group."""
    print('list_projects_in_group', 'group_id', group_id)
    project_ids: Any = []
    resource = f"{API_URL}/groups/{_url_escape(group_id)}/projects"
    status, response = do_request(token, "GET", resource)
    if response:
        project_ids.extend(project["id"] for project in json.loads(response))
    return status, project_ids


def create_project(
        token: str, parent_id: str, name: str) -> Tuple[int, Any]:
    """Create a repository into a parent."""
    print('create_project', 'parent_id', parent_id, 'name', name)
    resource = (
        f"{API_URL}/projects"
        f"?name={_url_escape(name)}"
        f"&path={_valid_path(name)}"
        f"&namespace_id={_url_escape(parent_id)}"

        # disable non-git-native things
        f"&lfs_enabled=false"
        f"&jobs_enabled=false"
        f"&wiki_enabled=false"
        f"&issues_enabled=false"
        f"&snippets_enabled=false"
        f"&merge_requests_enabled=false"
        f"&shared_runners_enabled=false"
        f"&container_registry_enabled=false")
    status, response = do_request(token, "POST", resource)
    if response:
        response = json.loads(response)["http_url_to_repo"]
    return status, response


def main():
    """Usual entry point."""
    # credentials and configurations
    user = get_key('analytics_gitlab_user')
    token = get_key('analytics_gitlab_token')
    customers_group_id = get_key('analytics_gitlab_customers_group_id')

    # mirror all subscriptions and repositories
    subs = map(lambda x: x.replace('/git/', ''), glob('/git/*'))
    for sub in subs:
        _, sub_id = get_group(token, f'fluidattacks/customer/{sub}')
        if not sub_id:
            # Create the group
            _, sub_id = create_group(token, customers_group_id, sub)
        for _proj in glob(f'/git/{sub}/*'):
            proj = _proj.replace(f'/git/{sub}/', '')
            _, _, proj_url = get_project(
                token, f'fluidattacks/customer/{sub}/{proj}')
            if not proj_url:
                # Create the project
                _, proj_url = create_project(token, sub_id, proj)
            if proj_url:
                proj_url = proj_url.replace(
                    'https://', f'https://{user}:{token}@')
                os.system(
                    f"git -C '/git/{sub}/{proj}' push --all '{proj_url}'")


if __name__ == "__main__":
    main()
