from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fx_tests.get_conf import (
    get_conf,
)
from google_sheets_etl.bin_sdk.tap import (
    TapGoogleSheets,
)
from google_sheets_etl.utils.temp_file import (
    TempFile,
)


def test_conf() -> None:
    assert get_conf()
    assert get_conf() == get_conf()


def test_discovery() -> None:
    tmp = TempFile.new()
    cmd = tmp.bind(
        lambda f: f.write_hook(
            lambda h: TapGoogleSheets.new(get_conf())
            .discover(h, None)
            .map(lambda r: r.unwrap())
            + Cmd.from_cmd(lambda: print(f.path))
        )
    )
    assert unsafe_unwrap(cmd)
