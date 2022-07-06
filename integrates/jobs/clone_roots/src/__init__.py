from contextlib import (
    suppress,
)
import http.client
import json
import logging
from typing import (
    Any,
    Optional,
)


def get_roots(token: str, group_name: str) -> Optional[dict[str, Any]]:
    conn = http.client.HTTPSConnection("app.fluidattacks.com")
    query = """
        query GetRootUpload($groupName: String!) {
            group(groupName: $groupName) {
              roots {
                ... on GitRoot {
                  id
                  nickname
                  uploadUrl
                  branch
                  url
                  credentials {
                    id
                    user
                    password
                    token
                    key
                  }
                  state
                }
              }
            }
        }
    """
    payload = {"query": query, "variables": {"groupName": group_name}}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/api", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    with suppress(json.decoder.JSONDecodeError):
        result = json.loads(data.decode("utf-8"))
        if "errors" in result:
            logging.error(result["errors"])
            return None
        return result
    return None


def update_root_cloning_status(  # pylint: disable=too-many-arguments
    token: str,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
    commit: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    conn = http.client.HTTPSConnection("app.fluidattacks.com")
    query = """
        mutation MeltsUpdateRootCloningStatus(
          $groupName: String!
          $rootId: ID!
          $status: CloningStatus!
          $message: String!
          $commit: String
        ) {
          updateRootCloningStatus(
            groupName: $groupName
            id: $rootId
            status: $status
            message: $message
            commit: $commit
          ) {
            success
          }
        }
    """
    payload = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "rootId": root_id,
            "status": status,
            "message": message,
            "commit": commit,
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/api", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    with suppress(json.decoder.JSONDecodeError):
        result = json.loads(data.decode("utf-8"))
        if "errors" in result:
            logging.error(result["errors"])
            return None
        return result
    return None
