from fa_purity import (
    Cmd,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.json.factory import (
    loads,
)
from google_sheets_etl.bin_sdk.tap import (
    decode_conf,
    TapConfig,
)
from google_sheets_etl.utils.cache import (
    Cache,
)
from google_sheets_etl.utils.process import (
    RunningSubprocess,
    Subprocess,
)
from google_sheets_etl.utils.temp_file import (
    TempFile,
)

_cache: Cache[TapConfig] = Cache(None)


def get_conf() -> TapConfig:
    out = TempFile.new()

    def save(file: TempFile) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            with file.path.open("w") as f:
                process = RunningSubprocess.run_universal_newlines(
                    Subprocess(
                        ("sops", "-d", "./fx_tests/secrets/conf.json"),
                        None,
                        f,
                        None,
                    )
                )
                result = unwrapper.act(process.bind(lambda p: p.wait(None)))
                if result == 0:
                    return
                raise Exception(
                    f"Sops call return code error != 0 i.e. code {result}"
                )

        return Cmd.new_cmd(_action)

    raw: Cmd[TapConfig] = (
        out.bind(lambda f: save(f).map(lambda _: f))
        .bind(lambda f: f.read_lines().to_list().map("".join))
        .map(loads)
        .map(lambda r: r.alt(Exception).bind(decode_conf).unwrap())
    )
    return _cache.get_or_set(raw)
