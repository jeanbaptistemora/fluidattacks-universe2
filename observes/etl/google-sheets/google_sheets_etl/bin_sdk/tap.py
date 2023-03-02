from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    JsonObj,
    JsonValue,
    Result,
    ResultE,
    UnfoldedJVal,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.json.transform import (
    dumps,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from google_sheets_etl.utils.cache import (
    Cache,
)
from google_sheets_etl.utils.process import (
    RunningSubprocess,
    Stdout,
    Subprocess,
)
from google_sheets_etl.utils.temp_file import (
    TempFile,
    TempReadOnlyFile,
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
        data: FrozenDict[str, UnfoldedJVal] = FrozenDict(
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
        return from_unfolded_dict(data)

    def to_file(self) -> Cmd[TempReadOnlyFile]:
        return TempReadOnlyFile.new(from_flist((dumps(self.to_json()),)))

    def __repr__(self) -> str:
        return "TapConfig: [masked]"


def decode_conf(raw: JsonObj) -> ResultE[TapConfig]:
    def get_str(key: str) -> ResultE[str]:
        return (
            Unfolder(JsonValue(raw))
            .uget(key)
            .bind(lambda u: u.to_primitive(str).alt(Exception))
        )

    def get_int(key: str) -> ResultE[int]:
        return (
            Unfolder(JsonValue(raw))
            .uget(key)
            .bind(lambda u: u.to_primitive(int).alt(Exception))
        )

    return get_str("client_id").bind(
        lambda client_id: get_str("client_secret").bind(
            lambda client_secret: get_str("refresh_token").bind(
                lambda refresh_token: get_str("spreadsheet_id").bind(
                    lambda spreadsheet_id: get_str("start_date").bind(
                        lambda start_date: get_str("user_agent").bind(
                            lambda user_agent: get_int("request_timeout").map(
                                lambda request_timeout: TapConfig(
                                    client_id,
                                    client_secret,
                                    refresh_token,
                                    spreadsheet_id,
                                    start_date,
                                    user_agent,
                                    request_timeout,
                                )
                            )
                        )
                    )
                )
            )
        )
    )


@dataclass(frozen=True)
class TapGoogleSheets:
    _private: _Private = field(repr=False, hash=False, compare=False)
    cache: Cache[TempFile] = field(repr=False, hash=False, compare=False)
    config: TapConfig

    @staticmethod
    def new(config: TapConfig) -> TapGoogleSheets:
        return TapGoogleSheets(_Private(), Cache(None), config)

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
