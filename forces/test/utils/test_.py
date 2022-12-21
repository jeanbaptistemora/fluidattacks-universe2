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
    check_policy_compliance,
    set_forces_exit_code,
)
import pytest


def test_check_policy_compliance() -> None:
    test_config = ForcesConfig(
        group="test_group",
        strict=True,
        breaking_severity=Decimal(5.0),
        grace_period=5,
    )
    compliant_vuln = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.OPEN,
        severity=Decimal("6.0"),
        report_date=(
            datetime.utcnow().replace(tzinfo=None) - timedelta(hours=5)
        ).isoformat(sep=" ", timespec="seconds"),
        exploitability=4.5,
        root_nickname=None,
    )
    assert check_policy_compliance(test_config, compliant_vuln)
    non_compliant_vuln = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.OPEN,
        severity=Decimal("6.0"),
        report_date=(
            datetime.utcnow().replace(tzinfo=None) - timedelta(days=10)
        ).isoformat(sep=" ", timespec="seconds"),
        exploitability=4.5,
        root_nickname=None,
    )
    assert not check_policy_compliance(test_config, non_compliant_vuln)


@pytest.mark.asyncio
async def test_set_exit_code() -> None:
    test_finding = Finding(
        identifier="dummy identifier",
        title="dummy title",
        state=FindingState.OPEN,
        exploitability=5.0,
        severity=Decimal("5.1"),
        url="https://dummy-url.com",
        vulnerabilities=[
            Vulnerability(
                type=VulnerabilityType.DAST,
                where="somewhere",
                specific="port 21",
                state=VulnerabilityState.OPEN,
                severity=Decimal("5.1"),
                report_date=(
                    datetime.utcnow().replace(tzinfo=None) - timedelta(hours=5)
                ).isoformat(sep=" ", timespec="seconds"),
                exploitability=5.0,
                root_nickname=None,
            )
        ],
    )
    test_config = ForcesConfig(
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
