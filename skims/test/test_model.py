# Third party libraries
import pytest

# Local libraries
from model import (
    core_model,
)
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)


@pytest.mark.skims_test_group('unittesting')
def test_model_core_model_manifest() -> None:
    ready: str = '\n'.join(sorted(
        finding.name
        for finding in core_model.FindingEnum
        if finding.value.auto_approve
    )) + '\n'
    in_dev: str = '\n'.join(sorted(
        finding.name
        for finding in core_model.FindingEnum
        if not finding.value.auto_approve
    )) + '\n'

    ready_path = 'skims/manifests/findings.lst'
    in_dev_path = 'skims/manifests/findings.dev.lst'

    if SHOULD_UPDATE_TESTS:
        for path, expected in (
            (in_dev_path, in_dev),
            (ready_path, ready),
        ):
            with open(path, 'w') as handle_w:
                handle_w.write(expected)

    for path, expected in (
        (in_dev_path, in_dev),
        (ready_path, ready),
    ):
        with open(path) as handle_r:
            assert handle_r.read() == expected
