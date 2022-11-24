from datetime import (
    datetime,
    timedelta,
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
    set_forces_exit_code,
)
import pytest


@pytest.mark.asyncio
async def test_set_exit_code() -> None:
    test_finding = Finding(
        identifier="dummy identifier",
        title="dummy title",
        state=FindingState.OPEN,
        exploitability=5.0,
        severity=5.1,
        url="https://dummy-url.com",
        vulnerabilities=[
            Vulnerability(
                type=VulnerabilityType.DAST,
                where="somewhere",
                specific="port 21",
                state=VulnerabilityState.OPEN,
                severity=5.1,
                report_date=(datetime.utcnow() - timedelta(hours=5)).isoformat(
                    sep=" ", timespec="seconds"
                ),
                exploitability=5.0,
                root_nickname=None,
            )
        ],
    )
    test_config = ForcesConfig(
        group="test_group",
        strict=True,
        breaking_severity=5.0,
        grace_period=0,
    )
    assert (
        await set_forces_exit_code(
            config=test_config, findings=(test_finding,)
        )
        == 1
    )
