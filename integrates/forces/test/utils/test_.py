from datetime import (
    datetime,
    timedelta,
)
from decimal import (
    Decimal,
)
from forces.model import (
    Finding,
    FindingState,
    ForcesConfig,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.utils.strict_mode import (
    get_policy_compliance,
    set_breaking_severity,
    set_forces_exit_code,
)
import pytest
from zoneinfo import (
    ZoneInfo,
)

# Constants
TIMEZONE: ZoneInfo = ZoneInfo("America/Bogota")


def test_set_breaking_severity() -> None:
    assert set_breaking_severity(0.0, 5.0) == Decimal("0.0")
    assert set_breaking_severity(0.1, 5.0) == Decimal("0.1")
    assert set_breaking_severity(6.0, 4.0) == Decimal("4.0")
    assert set_breaking_severity(None, 0.0) == Decimal("0.0")
    assert set_breaking_severity(None, 5.0) == Decimal("5.0")
    assert set_breaking_severity(None, None) == Decimal("0.0")


def test_check_policy_compliance() -> None:
    test_config = ForcesConfig(
        organization="test_org",
        group="test_group",
        strict=True,
        breaking_severity=Decimal(5.0),
        grace_period=5,
    )
    compliant_vuln = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.VULNERABLE,
        severity=Decimal("6.0"),
        report_date=(datetime.now(tz=TIMEZONE) - timedelta(hours=5)),
        exploitability=4.5,
        root_nickname=None,
        compliance=True,
    )
    assert get_policy_compliance(
        config=test_config,
        report_date=compliant_vuln.report_date,
        severity=compliant_vuln.severity,
        state=compliant_vuln.state,
    )
    non_compliant_vuln = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.VULNERABLE,
        severity=Decimal("6.0"),
        report_date=(datetime.now(tz=TIMEZONE) - timedelta(days=10)),
        exploitability=4.5,
        root_nickname=None,
        compliance=False,
    )
    assert not get_policy_compliance(
        config=test_config,
        report_date=non_compliant_vuln.report_date,
        severity=non_compliant_vuln.severity,
        state=non_compliant_vuln.state,
    )


@pytest.mark.asyncio
async def test_set_exit_code() -> None:
    test_finding = Finding(
        identifier="dummy identifier",
        title="dummy title",
        state=FindingState.VULNERABLE,
        exploitability=5.0,
        severity=Decimal("5.1"),
        url="https://dummy-url.com",
        vulnerabilities=[
            Vulnerability(
                type=VulnerabilityType.DAST,
                where="somewhere",
                specific="port 21",
                state=VulnerabilityState.VULNERABLE,
                severity=Decimal("5.1"),
                report_date=(datetime.now(tz=TIMEZONE) - timedelta(hours=5)),
                exploitability=5.0,
                root_nickname=None,
                compliance=False,
            )
        ],
    )
    test_config = ForcesConfig(
        organization="test_org",
        group="test_group",
        strict=True,
        breaking_severity=Decimal(5.0),
        grace_period=0,
    )
    assert (
        await set_forces_exit_code(
            config=test_config, findings=(test_finding,)
        )
        == 1
    )
