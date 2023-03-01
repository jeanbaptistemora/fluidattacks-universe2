from ._ro_file import (
    TempFile,
    TempReadOnlyFile,
)
from ._run import (
    RunningSubprocess,
    Stdout,
    Subprocess,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    JsonObj,
    Result,
    ResultE,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.json.transform import (
    dumps,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from google_sheets_etl._cache import (
    Cache,
)
from pathlib import (
    Path,
)
import sys


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class TapConfig:
    client_id: str
    client_secret: str
    refresh_token: str
    spreadsheet_id: str
    start_date: str
    user_agent: str
    request_timeout: int

    def to_json(self) -> JsonObj:
        return from_prim_dict(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "spreadsheet_id": self.spreadsheet_id,
                "start_date": self.start_date,
                "user_agent": self.user_agent,
                "request_timeout": self.request_timeout,
            }
        )

    def to_file(self) -> Cmd[TempReadOnlyFile]:
        return TempReadOnlyFile.new(from_flist((dumps(self.to_json()),)))


@dataclass(frozen=True)
class TapGoogleSheets:
    _private: _Private = field(repr=False, hash=False, compare=False)
    cache: Cache[TempFile] = field(repr=False, hash=False, compare=False)
    config: TapConfig

    @property
    def config_file_path(self) -> Path:
        return self.cache.get_or_set(
            self.config.to_file().bind(lambda f: f.extract())
        ).path

    def discover(self) -> Cmd[ResultE[None]]:
        cmd = (
            "tap-google-sheets",
            "--config",
            self.config_file_path.resolve().as_posix(),
            "--discover",
        )
        process = RunningSubprocess.run_universal_newlines(
            Subprocess(cmd, None, sys.stdout, Stdout.STDOUT),
        )
        return_code = process.bind(lambda p: p.wait(None))
        return return_code.map(
            lambda c: Result.success(None)
            if c == 0
            else Result.failure(
                Exception(f"Process ended with return code: {c}")
            )
        )
