import pytest
from utils_test import (
    get_suite_config,
    skims,
)


@pytest.mark.skims_test_group("bad_api_token")
def test_bad_integrates_api_token(test_group: str) -> None:
    suite: str = "nothing_to_do"
    code, stdout, stderr = skims(
        "scan",
        "--token",
        "123",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 1
    assert "StopRetrying: Invalid API token" in stdout, stdout
    assert not stderr, stderr
