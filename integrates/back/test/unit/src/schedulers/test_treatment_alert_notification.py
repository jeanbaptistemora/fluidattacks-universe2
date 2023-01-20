from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers.treatment_alert_notification import (
    days_to_end,
    expiring_vulnerabilities,
    ExpiringDataType,
    findings_close_to_expiring,
    unique_emails,
)

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2022-12-07T00:00:00.0")
def test_days_to_end() -> None:
    assert (
        days_to_end(datetime.fromisoformat("2022-12-12T00:00:00+00:00")) == 5
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "finding_id",
    ],
    [
        [
            "463558592",
        ],
    ],
)
@freeze_time("2021-01-14T06:00:00.0")
async def test_expiring_vulnerabilities(
    finding_id: str,
) -> None:
    loaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    vulns = await expiring_vulnerabilities(loaders, finding)
    assert list(list(vulns.values())[0].values())[0] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
    ],
    [
        [
            "unittesting",
        ],
    ],
)
@freeze_time("2021-01-14T06:00:00.0")
async def test_findings_close_to_expiring(
    group_name: str,
) -> None:
    findings = await findings_close_to_expiring(get_new_context(), group_name)
    assert len(findings) == 2


@pytest.mark.parametrize(
    ["groups_data"],
    [
        [
            {
                "oneshottest": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "customer_manager@fluidattacks.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "integratesuser@gmail.com",
                    ),
                    "group_expiring_findings": {},
                },
                "unittesting": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "continuoushacking@gmail.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "unittest2@fluidattacks.com",
                    ),
                    "group_expiring_findings": {},
                },
            }
        ],
    ],
)
def test_unique_emails(
    groups_data: dict[str, ExpiringDataType],
) -> None:
    emails = unique_emails(dict(groups_data), ())
    assert len(emails) == 9
