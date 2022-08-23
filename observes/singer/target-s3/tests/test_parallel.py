from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter import (
    factory as PureIterFactory,
)
import pytest
from target_s3._parallel import (
    in_threads,
)
from time import (
    sleep,
)


def mock_job() -> Cmd[None]:
    return Cmd.from_cmd(lambda: sleep(1))


@pytest.mark.timeout(2)
def test_threads() -> None:
    jobs = PureIterFactory.from_range(range(10)).map(lambda _: mock_job())
    try:
        in_threads(jobs, 10).compute()
    except SystemExit as exit:  # NOSONAR
        assert exit.code == 0
