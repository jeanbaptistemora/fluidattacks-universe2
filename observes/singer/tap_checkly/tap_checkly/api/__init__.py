# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    NamedTuple,
    Union,
)

# Third party libraries

# Local libraries
from tap_checkly.api.alert_channels import (
    AlertChsApi,
    AlertChsPage,
)
from tap_checkly.api.auth import (
    Credentials,
)
from tap_checkly.api.checks import (
    CheckGroupsPage,
    ChecksApi,
    ChecksPage,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.api.dashboards import (
    DashboardsApi,
    DashboardsPage,
)
from tap_checkly.api.maintenace_windows import (
    MantWindowsApi,
    MantWindowsPage,
)


ApiPage = Union[
    AlertChsPage,
    CheckGroupsPage,
    ChecksPage,
    DashboardsPage,
    MantWindowsPage,
]


class ApiClient(NamedTuple):
    alerts: AlertChsApi
    checks: ChecksApi
    dashboards: DashboardsApi
    maintenance: MantWindowsApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = Client.new(creds)
        return cls(
            alerts=AlertChsApi.new(client),
            checks=ChecksApi.new(client),
            dashboards=DashboardsApi.new(client),
            maintenance=MantWindowsApi.new(client),
        )


__all__ = [
    'Credentials',
]
