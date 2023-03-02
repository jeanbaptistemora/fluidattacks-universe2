from fa_purity.cmd import (
    unsafe_unwrap,
)
from fx_tests.get_conf import (
    get_conf,
)
from google_sheets_etl.bin_sdk.tap import (
    TapGoogleSheets,
)


def test_conf() -> None:
    assert get_conf()
    assert get_conf() == get_conf()


def test_discovery() -> None:
    cmd = TapGoogleSheets.new(get_conf()).discover()
    assert unsafe_unwrap(cmd)
