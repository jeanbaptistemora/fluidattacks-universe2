from cli import (
    cli,
)
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import io
import pytest
from typing import (
    Tuple,
)
from utils.logs import (
    configure,
)


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            cli.main(args=list(args), prog_name="skims")
        except SystemExit as exc:  # NOSONAR
            code: int = exc.code

    try:
        return code, out_buffer.getvalue(), err_buffer.getvalue()
    finally:
        del out_buffer
        del err_buffer


def get_suite_config(suite: str) -> str:
    return f"skims/test/data/config/{suite}.yaml"


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
