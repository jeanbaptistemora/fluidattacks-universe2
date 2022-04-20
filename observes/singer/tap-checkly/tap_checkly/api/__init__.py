from __future__ import (
    annotations,
)

from tap_checkly.api.alert_channels import (
    AlertChsApi,
    AlertChsPage,
)
from tap_checkly.api.checks import (
    CheckGroupsPage,
    CheckId,
    CheckReportsPage,
    CheckResultsPage,
    ChecksApi,
    ChecksPage,
)
from tap_checkly.api.common import (
    Credentials,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.api.dashboards import (
    DashboardsApi,
    DashboardsPage,
)
from tap_checkly.api.env_vars import (
    EnvVarsApi,
    EnvVarsPage,
)
from tap_checkly.api.maintenace_windows import (
    MantWindowsApi,
    MantWindowsPage,
)
from tap_checkly.api.snippets import (
    SnippetsApi,
    SnippetsPage,
)
from typing import (
    NamedTuple,
    Union,
)

ApiPage = Union[
    AlertChsPage,
    CheckGroupsPage,
    CheckReportsPage,
    CheckResultsPage,
    ChecksPage,
    DashboardsPage,
    EnvVarsPage,
    MantWindowsPage,
    SnippetsPage,
]


class ApiClient(NamedTuple):
    alerts: AlertChsApi
    checks: ChecksApi
    dashboards: DashboardsApi
    maintenance: MantWindowsApi
    snippets: SnippetsApi
    env: EnvVarsApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = Client.new(creds)
        return cls(
            alerts=AlertChsApi.new(client),
            checks=ChecksApi.new(client),
            dashboards=DashboardsApi.new(client),
            env=EnvVarsApi.new(client),
            maintenance=MantWindowsApi.new(client),
            snippets=SnippetsApi.new(client),
        )


__all__ = [
    "CheckId",
    "Credentials",
]
