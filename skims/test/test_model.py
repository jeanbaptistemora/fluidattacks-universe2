import json
from model import (
    core_model,
)
import pytest
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)


@pytest.mark.skims_test_group("_")
def test_model_core_model_manifest() -> None:
    for queue in core_model.ExecutionQueue:
        path: str = f"skims/manifests/findings.{queue.name}.json"
        expected: str = (
            json.dumps(
                sorted(
                    finding.name
                    for finding in core_model.FindingEnum
                    if finding.value.execution_queue == queue
                ),
                indent=2,
            )
            + "\n"
        )

        if SHOULD_UPDATE_TESTS:
            with open(path, "w") as handle_w:
                handle_w.write(expected)

        with open(path) as handle_r:
            assert handle_r.read() == expected


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_from_integrates() -> None:
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.INPUTS,
        what_on_integrates="test",
    )
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.LINES,
        what_on_integrates="test",
    )
    assert ("", "test") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.PORTS,
        what_on_integrates="test",
    )
    assert ("ns", "test()") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.INPUTS,
        what_on_integrates="test() (ns)",
    )
    assert ("ns", "te/st") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.LINES,
        what_on_integrates="ns/te/st",
    )
    assert ("ns", "test()") == core_model.Vulnerability.what_from_integrates(
        kind=core_model.VulnerabilityKindEnum.PORTS,
        what_on_integrates="test() (ns)",
    )
