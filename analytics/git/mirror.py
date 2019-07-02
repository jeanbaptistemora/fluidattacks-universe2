#!/usr/bin/env python3
"""Mirror customer repositories to Gitlab."""

import os
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from typing import Tuple, Any

API_URL = "https://gitlab.com/api/v4"


def get_request(token: str, method: str, resource: str) -> Tuple[int, Any]:
    """Request a resource, return status and response."""
    status: int
    response: Any
    try:
        request = urllib.request.Request(
            resource,
            method=method,
            headers={"Private-Token": f"{token}"})
        connection = urllib.request.urlopen(request)

        status, response = 200, connection.read().decode('utf-8')
    except urllib.error.HTTPError as error:
        status, response = error.code, None
    except urllib.error.URLError:
        status, response = 0, None

    print("REQUEST:", method, resource, status, response)
    return (status, response)


def create_group(token: str, parent_id: str, name: str) -> Tuple[int, Any]:
    """Create a group into parent."""
    resource = (
        f"{API_URL}/groups"
        f"?name={name}"
        f"&path={name}"
        f"&parent_id={parent_id}")
    status, response = get_request(token, "POST", resource)
    return status, json.loads(response)["id"] if status == 200 else None


def delete_group(token: str, group_id: str) -> Tuple[int, Any]:
    """Delete a group if exist."""
    resource = f"{API_URL}/groups/{group_id}"
    status, response = get_request(token, "DELETE", resource)
    return status, response


def list_groups_in_group(token: str, group_id: str) -> Tuple[int, Any]:
    """List groups in a group."""
    group_ids: Any = []
    resource = f"{API_URL}/groups/{group_id}/subgroups"
    status, response = get_request(token, "GET", resource)
    if status == 200:
        group_ids.extend(group["id"] for group in json.loads(response))
    return status, group_ids


def create_repository(
        token: str, parent_id: str, name: str) -> Tuple[int, Any]:
    """Create a repository into a parent."""
    name = urllib.parse.quote(name, safe='')
    resource = (
        f"{API_URL}/projects"
        f"?name={name}"
        f"&namespace_id={parent_id}"

        # disable non-git-native things
        f"&lfs_enabled=false"
        f"&jobs_enabled=false"
        f"&wiki_enabled=false"
        f"&issues_enabled=false"
        f"&snippets_enabled=false"
        f"&merge_requests_enabled=false"
        f"&shared_runners_enabled=false"
        f"&container_registry_enabled=false")
    status, response = get_request(token, "POST", resource)
    if status == 200:
        response = json.loads(response)["http_url_to_repo"]
    return status, response


def main():
    """Usual entry point."""
    # pylint: disable=too-many-locals

    # credentials and configurations
    user = os.popen((
        f"vault read -field=analytics_gitlab_user "
        f"secret/serves")).read()
    token = os.popen((
        f"vault read -field=analytics_gitlab_token "
        f"secret/serves")).read()
    customers_group_id = os.popen((
        f"vault read -field=analytics_gitlab_customers_group_id "
        f"secret/serves")).read()

    # configuration file
    with open("/config.json") as config_file:
        configs = json.load(config_file)

    # list of todo's
    todo = {}
    for config in configs:
        try:
            todo[config["subscription"]].append(config["repository"])
        except KeyError:
            todo[config["subscription"]] = [config["repository"]]

    # delete all groups in group customers_group_id
    _, group_ids = list_groups_in_group(token, customers_group_id)
    for group_id in group_ids:
        delete_group(token, group_id)

    # mirror all subscription and repositories
    for subscription, repositories in todo.items():
        print("MIRRORING SUBSCRIPTION:", subscription)
        for _ in range(60):
            status, subscription_group_id = create_group(
                token, customers_group_id, subscription)
            if status == 200:
                break
            else:
                time.sleep(60.0)
        for repository in repositories:
            print("MIRRORING REPOSITORY:", subscription, repository)
            _, repo_url = create_repository(
                token, subscription_group_id, repository)
            repo_url = repo_url.replace('https://', f'https://{user}:{token}@')
            repo_path = f"/git/{subscription}/{repository}"

            os.system(f"git -C '{repo_path}' push --all '{repo_url}'")


if __name__ == "__main__":
    main()
