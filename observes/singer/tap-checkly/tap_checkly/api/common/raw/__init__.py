# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import logging
from paginator import (
    PageId,
)
from requests.exceptions import (
    HTTPError,
)
from returns.io import (
    IO,
)
from singer_io.singer2.json import (
    JsonObj,
    JsonValue,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from typing import (
    List,
)

LOG = logging.getLogger(__name__)


def _mask_env_var(env_var: JsonValue) -> JsonValue:
    new_env = env_var.to_json()
    new_env["value"] = JsonValue("__masked__")
    return JsonValue(new_env)


def _mask_env_vars(items: List[JsonObj]) -> List[JsonObj]:
    _items = items.copy()
    for item in _items:
        env_vars = item["environmentVariables"].to_opt_list()
        if env_vars:
            new_envs = [_mask_env_var(env_var) for env_var in env_vars]
            item["environmentVariables"] = JsonValue(new_envs)
    return _items


def list_reports(
    client: Client,
) -> IO[List[JsonObj]]:
    result = client.get("/v1/reporting")
    LOG.debug("reports response: %s", result)
    return IO(result)


def list_alerts_channels(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/alert-channels",
        params={"limit": page.per_page, "page": page.page},
    )
    LOG.debug("alert-channels response: %s", result)
    return IO(result)


def list_checks(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/checks", params={"limit": page.per_page, "page": page.page}
    )
    LOG.debug("checks response: %s", result)
    return IO(_mask_env_vars(result))


def list_check_groups(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/check-groups", params={"limit": page.per_page, "page": page.page}
    )
    LOG.debug("check-groups response: %s", result)
    return IO(_mask_env_vars(result))


def list_check_status(client: Client) -> IO[List[JsonObj]]:
    result = client.get("/v1/check-statuses")
    LOG.debug("check-status response: %s", result)
    return IO(result)


def list_dashboards(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/dashboards", params={"limit": page.per_page, "page": page.page}
    )
    LOG.debug("dashboards response: %s", result)
    return IO(result)


def list_env_vars(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = []
    try:
        result = client.get(
            "/v1/variables", params={"limit": page.per_page, "page": page.page}
        )
    except HTTPError as error:
        if error.response.status_code != 500:
            raise error
    for item in result:
        item["value"] = JsonValue("__masked__")
    LOG.debug("variables response: %s", result)
    return IO(result)


def list_mant_windows(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/maintenance-windows",
        params={"limit": page.per_page, "page": page.page},
    )
    LOG.debug("maintenance-windows response: %s", result)
    return IO(result)


def list_snippets(client: Client, page: PageId) -> IO[List[JsonObj]]:
    result = client.get(
        "/v1/snippets", params={"limit": page.per_page, "page": page.page}
    )
    LOG.debug("snippets response: %s", result)
    return IO(result)
